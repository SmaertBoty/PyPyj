#
# PyPyj v1.0.0
#
# PyPyj is a lightweight extension layer for Pyjinn that re‑implements selected 
# Python built‑in functions which are currently not supported natively by Pyjinn.
#
# https://github.com/Minescripters/PyPyj
#

File = JavaClass("java.io.File")
RandomAccessFile = JavaClass("java.io.RandomAccessFile")
BufferedWriter = JavaClass("java.io.BufferedWriter")
InputStreamReader = JavaClass("java.io.InputStreamReader")
OutputStreamWriter = JavaClass("java.io.OutputStreamWriter")
FileOutputStream = JavaClass("java.io.FileOutputStream")
ByteArrayOutputStream = JavaClass("java.io.ByteArrayOutputStream")
ByteArrayInputStream = JavaClass("java.io.ByteArrayInputStream")


# ======================
# open()
# ======================

class _File:
    path: str
    mode: str
    closed: bool
    _raf: object

    def __init__(self, path: str, mode: str) -> None:
        self.path = path
        self.mode = mode
        self.closed = False

        valid = ["r", "w", "a", "r+", "w+", "a+"]
        if mode not in valid:
            raise ValueError("Unsupported mode: " + mode)

        file_obj = File(path)

        if mode == "r":
            self._raf = RandomAccessFile(file_obj, "r")

        elif mode == "w":
            self._raf = RandomAccessFile(file_obj, "rw")
            self._raf.setLength(0)

        elif mode == "a":
            self._raf = RandomAccessFile(file_obj, "rw")
            self._raf.seek(self._raf.length())

        elif mode == "r+":
            self._raf = RandomAccessFile(file_obj, "rw")

        elif mode == "w+":
            self._raf = RandomAccessFile(file_obj, "rw")
            self._raf.setLength(0)

        elif mode == "a+":
            self._raf = RandomAccessFile(file_obj, "rw")
            self._raf.seek(self._raf.length())

    # ----------------------
    # READ

    def read(self, size: int | None = None) -> str:
        self._check_closed()

        if size is not None:
            if not isinstance(size, int):
                raise TypeError("size must be int or None")
            if size <= 0:
                return ""

        baos = ByteArrayOutputStream()

        if size is None:
            while True:
                b = self._raf.read()
                if b == -1:
                    break
                baos.write(b)
        else:
            count = 0
            while count < size:
                b = self._raf.read()
                if b == -1:
                    break
                baos.write(b)
                count += 1

        byte_array = baos.toByteArray()

        bais = ByteArrayInputStream(byte_array)
        reader = InputStreamReader(bais, "UTF-8")

        result = []
        while True:
            ch = reader.read()
            if ch == -1:
                break
            result.append(chr(ch))

        reader.close()

        return "".join(result)

    def readline(self) -> str:
        self._check_closed()

        line = self._raf.readLine()
        if line is None:
            return ""
        return line + "\n"

    def readlines(self) -> list[str]:
        lines = []
        while True:
            line = self.readline()
            if line == "":
                break
            lines.append(line)
        return lines

    # ----------------------
    # WRITE

    def write(self, text: str) -> None:
        self._check_closed()

        if not isinstance(text, str):
            raise TypeError("write() argument must be str")

        self._raf.close()

        fos = FileOutputStream(self.path, True)
        writer = BufferedWriter(OutputStreamWriter(fos, "UTF-8"))

        writer.write(text)
        writer.flush()
        writer.close()

        self._raf = RandomAccessFile(File(self.path), "rw")
        self._raf.seek(self._raf.length())

    def writelines(self, iterable: list[str] | tuple[str, ...] | object) -> None:
        for item in iterable:
            self.write(item)

    # ----------------------
    # POSITION

    def seek(self, offset: int) -> None:
        self._check_closed()
        self._raf.seek(offset)

    def tell(self) -> int:
        self._check_closed()
        return self._raf.getFilePointer()

    # ----------------------
    # OTHER

    def close(self) -> None:
        if not self.closed:
            self._raf.close()
            self.closed = True

    def _check_closed(self) -> None:
        if self.closed:
            raise ValueError("I/O operation on closed file.")


def open(path: str, mode: str = "r") -> _File:
    return _File(path, mode)


# ======================
# pow()
# ======================

def pow(x: int | float, y: int | float, mod: int | None = None) -> int | float:
    if mod is None:
        return x ** y

    if not isinstance(x, int) or not isinstance(y, int) or not isinstance(mod, int):
        raise TypeError("pow() 3rd argument not allowed unless all arguments are integers")

    if mod == 0:
        raise ValueError("pow() 3rd argument cannot be 0")

    result = 1
    base = x % mod
    exp = y

    if exp < 0:
        raise ValueError("pow() 2nd argument cannot be negative when 3rd argument specified")

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp = exp // 2

    return result


# ======================
# bin() y oct()
# ======================

def _to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    num = n

    while num > 0:
        result = digits[num % base] + result
        num = num // base

    return result


def bin(x: int) -> str:
    if not isinstance(x, int):
        raise TypeError("bin() argument must be int")

    if x < 0:
        return "-0b" + _to_base(-x, 2)
    return "0b" + _to_base(x, 2)


def oct(x: int) -> str:
    if not isinstance(x, int):
        raise TypeError("oct() argument must be int")

    if x < 0:
        return "-0o" + _to_base(-x, 8)
    return "0o" + _to_base(x, 8)


# ======================
# all() y any()
# ======================

def all(iterable: object) -> bool:
    for item in iterable:
        if not item:
            return False
    return True


def any(iterable: object) -> bool:
    for item in iterable:
        if item:
            return True
    return False


# ======================
# reversed()
# ======================

def reversed(iterable: str | list[object] | object) -> str | list[object]:
    if isinstance(iterable, str):
        result = ""
        i = len(iterable) - 1
        while i >= 0:
            result += iterable[i]
            i -= 1
        return result

    if isinstance(iterable, list):
        new_list = iterable.copy()
        new_list.reverse()
        return new_list

    new_list = list(iterable)
    new_list.reverse()
    return new_list


# ======================
# sorted()
# ======================

def sorted(iterable: list[object] | tuple[object, ...] | object, reverse: bool = False) -> list[object]:
    new_list = list(iterable)
    new_list.sort()
    if reverse:
        new_list.reverse()
    return new_list
