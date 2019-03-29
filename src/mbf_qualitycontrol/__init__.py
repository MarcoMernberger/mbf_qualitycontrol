import pypipegraph as ppg

def ensure_collector():
    if not hasattr(ppg.util.global_pipegraph, '_global_qc_collector'):
        ppg.util.global_pipegraph._global_qc_collector = {}
    return ppg.util.global_pipegraph._global_qc_collector




def register_qc(name, qc_object):
    if name in ensure_collector():
        raise KeyError("Duplicate name: %s" % name)
    if not hasattr(qc_object, 'get_qc_job'):
        raise ValueError('not a qc object')
    qc_object.name = name
    ensure_collector()[name] = qc_object

def get_qc(name):
    return ensure_collector()[name]


def do_qc():
    jobs = []
    for v in ensure_collector().values():
        jobs.append(v.get_qc_job())
    return jobs


class QCCallback:
    def __init__(self, callback):
        if not hasattr(callback, '__call__'):
            raise ValueError("callback must be a callable")
        self.callback = callback

    def get_qc_job(self):
        return self.callback()

