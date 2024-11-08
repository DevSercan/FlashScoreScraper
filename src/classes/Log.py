import time # Used for 'time information and delaying the software' operations.
import traceback # Displays current error details for debugging.
import os
from src.utils.helper import getConfig

CONFIG = getConfig()
PATH = str(CONFIG["logging"]["path"])
LEVEL = int(CONFIG["logging"]["minimumLevel"])
SIZE = int(CONFIG["logging"]["fileSizeLimitMegabytes"])
PRINTCONSOLE = bool(CONFIG["logging"]["printLogsToConsole"])

class Log:
    """ A class used to colorize console outputs. """
    def __init__(self, printConsole:bool=PRINTCONSOLE, logFolder:str=PATH, logLevel:int=LEVEL, maxFileSizeMB:int=SIZE):
        """ Function used for log entries. """
        if not 1 <= logLevel <= 5:
            raise ValueError("'logLevel' value must be between 1 and 5.")
        self.printConsole = printConsole
        self.logFolder = logFolder
        self.logLevel = logLevel
        self.maxFileSizeMB = maxFileSizeMB
        self.levelTags = {1: "[CRITICAL]", 2: "[ERROR]", 3: "[WARNING]", 4: "[INFO]", 5: "[DEBUG]"}
        if not os.path.exists(self.logFolder):
            os.makedirs(self.logFolder)

    def _log(self, message:str, level:int):
        try:
            if level <= self.logLevel:
                filePath = self._getLastLogFile()
                if os.path.exists(filePath):
                    currentSize = os.path.getsize(filePath) / (1024*1024) # Retrieves file size in MB.
                    if currentSize > self.maxFileSizeMB: # If the file size exceeds the target size, creates a new log file.
                        self.createLogFile()
                    del currentSize
                logTime = time.strftime("[%d.%m.%Y %H:%M:%S]") # Stores the current time as a string in the format 'day.month.year hour:minute:second'.
                logText = f"{logTime} {self.levelTags[level]} {message}"
                if self.printConsole and level != 5: # Condition is met if the option to print log entries to the console is True AND the log message level to be printed is not Debug.
                    print(logText) # Prints the log entry to the console.
                with open(filePath, "a", encoding="utf-8") as file: # Appends to the file if it exists. If not, creates it.
                    file.write(f"{logText}\n")
                del logTime, logText
        except Exception as e:
            errorName = type(e).__name__ # Retrieves the name of the caught error as a string.
            errorMessage = f"[{errorName}]\n{traceback.format_exc()}"
            with open(filePath, "a", encoding="utf-8") as file:
                file.write(f"LogError: {errorMessage}\n")
    
    def createLogFile(self) -> str:
        fileName = time.strftime("log_%d%m%Y-%H%M%S.log") # Stores the file name as 'log_dayMonthYear-HourMinute.log'.
        filePath = os.path.join(self.logFolder, fileName)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write("")
        del fileName
        return filePath

    def _getLastLogFile(self) -> str:
        if not os.path.exists(self.logFolder):
            os.makedirs(self.logFolder)
        if len(os.listdir(self.logFolder)) < 1:
            self.createLogFile()
        fullLogPaths = [os.path.join(self.logFolder, file) for file in os.listdir(self.logFolder)]
        lastLogFile = max(fullLogPaths, key=os.path.getctime)
        del fullLogPaths
        return lastLogFile

    def critical(self, message:str):
        """ Used for logging at a critical level. """
        self._log(message, 1)

    def error(self, message:str):
        """ Used for logging at an error level. """
        self._log(message, 2)

    def warning(self, message:str):
        """ Used for logging at a warning level. """
        self._log(message, 3)

    def info(self, message:str):
        """ Used for logging at an information level. """
        self._log(message, 4)

    def debug(self, message:str):
        """ Used for logging at a debug level. Contains code details. """
        self._log(message, 5)