from hashlib import md5
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

from ..path import cache_path
from ..core import BaseSequence


class SyntheticFloodSequence(BaseSequence):
    """A base class for generating synthetic sequences of streamflow
    """

    def __init__(self, **kwargs) -> None:
        seq_param = {"n_seq": kwargs.pop("n_seq")}
        super().__init__(category="SyntheticFloodSequence", **kwargs)
        self.param.update(seq_param)
        self.model_name = ""

    def _calculate_one(self) -> np.ndarray:
        """This *must* be implemented by a specific child class
        """
        raise NotImplementedError

    def _calculate_all(self) -> xr.DataArray:
        """Just loop through and combine
        """
        sequences = 1 + np.arange(self.param.get("n_seq"))
        sflow = xr.concat(
            [
                xr.DataArray(
                    data=self._calculate_one(),
                    coords={"year": self._get_time("all")},
                    dims="year",
                    name="Synthetic Streamflow Sequence",
                )
                for seq in sequences
            ],
            dim="sequence",
        )
        sflow["sequence"] = sequences
        sflow.attrs = self._get_attributes()
        return sflow

    def _get_filename(self) -> str:
        """Get a file name

        Uses the parameters of the model to build a dictionary of all the
        key attributes of the model. Then converts them to a string
        and hashes the output to a (shorter!) filename. Finally adds the path
        to the data directory and the appropriate file suffix.
        """

        attributes = self._get_attributes()
        _ = [attributes.pop(var) for var in ["M", "N"]]

        file_string = ""
        for key, val in attributes.items():
            file_string += "_{}={}".format(key, val)

        file_string = md5(file_string.encode("ascii")).hexdigest()
        file_string += ".nc"

        file_dir = os.path.join(cache_path, self.category)
        file_dir = os.path.abspath(file_dir)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        filename = os.path.abspath(os.path.join(file_dir, file_string))
        return filename

    def _from_file(self) -> Tuple[xr.DataArray, bool]:
        """Get data from file

        NEEDS TO B
        """
        try:
            data = xr.open_dataarray(self._get_filename())
            attr_observed = data.attrs
            M_observed = attr_observed.pop("M")
            N_observed = attr_observed.pop("N")
            attr_desired = self._get_attributes()
            M_desired = attr_desired.pop("M")
            N_desired = attr_desired.pop("N")
            success = False  # default assumption is no luck
            if (
                (attr_desired == attr_observed)
                and (M_observed >= M_desired)
                and (N_observed >= N_desired)
            ):
                data = data.sel(year=slice(1 - N_desired, M_desired))
                success = True  # we did it!
            else:
                data = None  # no luck

        except BaseException:
            success = False
            data = None

        return data, success

    def lineplot(self, **kwargs) -> None:
        """Create a line plot of simulated sequences
        """
        sequences = self.data
        sequences = sequences.sel(year=self._get_time(kwargs.pop("period", "all")))
        fig, ax = plt.subplots(figsize=(10, 5), nrows=1, ncols=1)
        for s in np.arange(self.param.get("n_seq")):
            sequences.sel(sequence=(s + 1)).plot(
                ax=ax,
                c=kwargs.pop("c", "blue"),
                linewidth=kwargs.pop("linewidth", 0.25),
            )
            ax.set_ylim([sequences.min(), sequences.max()])
            ax.semilogy()
            ax.set_title(self.model_name)
        fig.tight_layout()
