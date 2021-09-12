'''
The MIT License (MIT)

Copyright (c) 2021 Tom-the-Bomb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

class TioResponse:

    def __init__(self, data: str) -> None:

        self.token = data[:16]
        
        data = data.replace(data[:16], "")
        self.output = data

        stats = data.split("\n")
        parse_line = lambda line: line.split(":")[-1].strip().split(" ")[0]

        try:
            self.stdout      = "\n".join(stats[:-5])
            self.real_time   = parse_line(stats[-5])
            self.user_time   = parse_line(stats[-4])
            self.sys_time    = parse_line(stats[-3])
            self.cpu_usage   = parse_line(stats[-2])
            self.exit_status = parse_line(stats[-1])
        except IndexError:
            pass

    def __repr__(self) -> str:
        return f"<TioResponse status={self.exit_status}>"

    def __str__(self) -> str:
        return self.output

    def __int__(self) -> int:
        return self.exit_status

    def __eq__(self, o) -> bool:
        if isinstance(o, TioResponse):
            return self.stdout == o.stdout
        else:
            return self.stdout == o
        
    def __ne__(self, o) -> bool:
        return not self.__eq__(o)