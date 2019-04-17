import pypipegraph as ppg


def ensure_collector():
    if not hasattr(ppg.util.global_pipegraph, "_global_qc_collector"):
        ppg.util.global_pipegraph._global_qc_collector = {}
    return ppg.util.global_pipegraph._global_qc_collector


def register_qc(name, qc_object):
    if not ppg.inside_ppg():  # pragma: no cover
        return
    if hasattr(ppg.util.global_pipegraph, "_global_qc_started"):
        raise ValueError(
            "trying to register qc without pipegraph or after do_qc has started"
        )
    if name in ensure_collector():
        raise KeyError("Duplicate name: %s" % name)
    if not hasattr(qc_object, "get_qc_job"):
        raise TypeError("not a qc object")
    qc_object.name = name
    ensure_collector()[name] = qc_object
    return qc_object


def get_qc(name):
    return ensure_collector()[name]


def do_qc(filter_by_name=lambda name: True):
    jobs = []
    collected = ensure_collector()
    ppg.util.global_pipegraph._global_qc_started = True
    del ppg.util.global_pipegraph._global_qc_collector
    for name, v in collected.items():
        if filter_by_name(name):
            jobs.append(v.get_qc_job())
    return jobs


class QCCallback:
    """Just a slightly fancy wrapper around a callback returning a ppg.Job"""

    def __init__(self, callback):
        if not hasattr(callback, "__call__"):
            raise ValueError("callback must be a callable")
        self.callback = callback

    def get_qc_job(self):
        return self.callback()


class no_qc:
    """When you want some objects not to register their qc - e.g. for testing

    Use as context manager
    with no_qc():
        lane = mbf_aligned.lanes.Lane(...)
    """

    def __enter__(self):
        self.old_collector = ensure_collector()
        ppg.util.global_pipegraph._global_qc_collector = {}
        return ppg.util.global_pipegraph._global_qc_collector

    def __exit__(self, *args):
        ppg.util.global_pipegraph._global_qc_collector = self.old_collector


def QCCollector(output_filename, job_func, element):
    """A qc that collects elements and plots them all at once"""
    try:
        q = get_qc(output_filename)
    except KeyError:
        q = _QCCollector(job_func)
        register_qc(output_filename, q)
    q.add(element)
    return q


class _QCCollector:
    """A qc that collects elements and plots them all at once"""

    def __init__(self, callback):
        self.elements = []
        self.callback = callback

    def add(self, element):
        self.elements.append(element)

    def get_qc_job(self):
        return self.callback(self.elements)
