import gzip
import shutil
from pathlib import Path


class CompressionService:

    @staticmethod
    def compress(file_path: str) -> str:
        """
        Compress a file using gzip.
        Returns compressed file path.
        """

        input_path = Path(file_path)
        output_path = input_path.with_suffix(input_path.suffix + ".gz")

        with open(input_path, "rb") as f_in:
            with gzip.open(output_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        return str(output_path)

    @staticmethod
    def decompress(file_path: str) -> str:
        """
        Decompress gzip file.
        Returns decompressed file path.
        """

        input_path = Path(file_path)
        output_path = input_path.with_suffix("")

        with gzip.open(input_path, "rb") as f_in:
            with open(output_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        return str(output_path)
