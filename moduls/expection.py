# exceptions.py

class DownloaderError(Exception):
    """Base exception for the downloader library."""
    pass


class InvalidURL(DownloaderError):
    """Raised when the input URL is invalid or unsupported."""
    pass


class DownloadFailed(DownloaderError):
    """Raised when the download process fails."""
    pass


class NetworkError(DownloaderError):
    """Raised when a network connection error occurs."""
    pass


class FileWriteError(DownloaderError):
    """Raised when the downloaded file cannot be written."""
    pass
