from enum import Enum
import os


class PATHS(Enum):
    # train data directory which was provided
    CSV_DIR = os.path.join(os.path.dirname(__file__), ".." ,"..", "original_data", "stock_price_data_files")

    # test data directory which will be generated
    CSV_MODIFIED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "modified_data")


class TYPE_OF_DATA(Enum):
    # type of data which can be used for training
    ORIGINAL = "ORIGINAL",
    # type of data which can be used for testing
    MODIFIED = "MODIFIED"