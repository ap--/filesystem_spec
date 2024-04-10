import itertools
import random
import string

from fsspec import get_filesystem_class

random.seed(0)


def _make_random_path():
    pth_len = random.randint(5, 40)
    return "".join(random.sample(string.ascii_letters + "/", k=pth_len))


def _make_uris(n):
    it_proto_netloc = itertools.cycle(
        itertools.product(["file", "local", "wrong", None], ["netloc", ""])
    )

    for _ in range(n):
        proto, netloc = next(it_proto_netloc)
        pth = _make_random_path()
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
