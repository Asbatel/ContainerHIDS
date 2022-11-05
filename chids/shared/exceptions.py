class NoSyscallsFound(Exception):

    def __init__(self, scap, message="The scap has no syscalls"):
        self.scap = scap
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.scap} -> {self.message}'
    pass


class CorruptedFile(Exception):

    def __init__(self, scap, message="The scap file is either corrupted or no data has been written"):
        self.scap = scap
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.scap} -> {self.message}'
    pass