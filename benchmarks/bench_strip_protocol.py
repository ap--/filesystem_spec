import itertools
import random
import string

from fsspec import get_filesystem_class

random.seed(0)


def _make_random_path(style):
    pth_len = random.randint(5, 40)
    if style == "posix":
        chars = string.ascii_letters + "/"
        prefix = ""
    elif style == "win":
        chars = string.ascii_letters + "\\"
        prefix = "c:\\"
    elif style == "win-posix":
        chars = string.ascii_letters + "/"
        prefix = "c:/"
    else:
        raise ValueError(f"Unknown style {style}")
    return prefix + "".join(random.sample(chars, k=pth_len))


def _make_uris(n):
    it_proto_netloc_style = itertools.cycle(
        itertools.product(
            ["file", "local", "wrong", None],
            ["netloc", ""],
            ["posix", "win", "win-posix"],
        )
    )

    for _ in range(n):
        proto, netloc, style = next(it_proto_netloc_style)
        pth = _make_random_path(style)
        if proto and netloc:
            yield f"{proto}://{netloc}/{pth}"
        elif proto:
            yield f"{proto}:/{pth}"
        else:
            yield f"{netloc}/{pth}"


uris = list(_make_uris(10000))


class Suite:
    def setup(self):
        self.fs_cls = get_filesystem_class("file")
        self.uris = uris

    def teardown(self):
        del self.uris

    def time_split_protocol(self):
        for uri in self.uris:
            self.fs_cls._strip_protocol(uri)

    def time_parent(self):
        for uri in self.uris:
            self.fs_cls._parent(uri)
