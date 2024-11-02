from torch.cuda import is_available


def get_device():
    return 0 if is_available() else -1
