

def add_to_histogram(sum_hist, current_hist, weight):
    orig = sum_hist.getArray()
    current = current_hist.getArray()
    res = orig + weight*current
    sum_hist.setContent(res)


def apply_mask_to_histogram(histogram, mask_hist):
    for i in range(0, histogram.getTotalNumberOfBins()):
        if mask_hist.getBinContent(i) == 1:
            histogram.setBinContent(i, 0)
