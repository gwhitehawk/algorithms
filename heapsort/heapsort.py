# python heapsort.py -f <input_file>
# Sorts comma-separated list of numbers by heapsort.
# Prints min-heap.

import click
import math
import time
import sys


def animate(f):
    def wrap_print(*args, **kwargs):
        sys.stdout.write("\r" + ' '.join([str(el) for el in f(*args, **kwargs)]))
        sys.stdout.flush()
        time.sleep(0.5)
    return wrap_print


class Heap(object):
    def __init__(self):
        self.heap = []

    def get_parent(self, index):
        return (index - 1)/2

    def get_min_child(self, cur, cur_len):
        left_child = 2 * cur + 1
        right_child = 2 * cur + 2
        min_child = 0
        if left_child <= cur_len:
            min_child = left_child
        if right_child <= cur_len and self.heap[right_child] < self.heap[left_child]:
            min_child = right_child
        return min_child

    @animate
    def swap(self, first, second):
        val = self.heap[first]
        self.heap[first] = self.heap[second]
        self.heap[second] = val
        return self.heap

    @animate
    def append(self, element):
        self.heap.append(element)
        return self.heap

    def insert(self, element):
        self.append(element)
        cur = len(self.heap) - 1
        parent = self.get_parent(cur)
        while cur > 0 and self.heap[cur] < self.heap[parent]:
            self.swap(cur, parent)
            cur = parent
            parent = self.get_parent(parent)

    def extract_min(self, cur_len):
        self.swap(0, cur_len)
        cur = 0
        min_child = self.get_min_child(0, cur_len - 1)
        while min_child > 0 and self.heap[cur] > self.heap[min_child]:
            self.swap(cur, min_child)
            cur = min_child
            min_child = self.get_min_child(min_child, cur_len - 1)

    def build_heap(self, unsorted):
        print 'Building the heap:'
        for elem in unsorted:
            self.insert(elem)

    def print_heap(self):
        print '\nThe heap:'
        height = int(math.ceil(math.log(len(self.heap), 2)))
        cur_width = 1
        cur_offset = 0
        floor = 1
        while cur_offset < len(self.heap):
            last = min(len(self.heap), cur_offset + cur_width)
            cur_x = 0
            cur_row = ''
            for i in range(cur_offset, last):
                next_x = 3 * (i - cur_offset) * 2**(height - floor)
                cur_row += ''.join([' ' for j in range(cur_x, next_x)])
                cur_row += str(self.heap[i])
                cur_x = next_x + len(str(self.heap[i]))
            print cur_row
            cur_offset = cur_offset + cur_width
            cur_width = 2 * cur_width
            floor += 1

    def deconstruct(self):
        print 'Sorting the heap:'
        cur_len = len(self.heap) - 1
        while cur_len > 0:
            self.extract_min(cur_len)
            cur_len -= 1

    def sort(self, unsorted):
        self.build_heap(unsorted)
        self.print_heap()
        self.deconstruct()


@click.command()
@click.option("-f", "--filename", help="input file name")
def main(filename):
    with open(filename, "r") as f:
        unsorted = [int(el) for el in f.read().strip().split(',')]
        heap = Heap()
        heap.sort(unsorted)
        print '\r'


if __name__ == '__main__':
    main()
