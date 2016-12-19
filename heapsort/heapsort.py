# python heapsort.py -f <input_file>
# Sorts comma-separated list of numbers by heapsort.
# Prints min-heap.

import click
import math

class Heap(object):
    def __init__(self):
        self.heap = []

    def get_parent(self, index):
        return (index - 1)/2

    def get_min_child(self, cur):
        left_child = 2*cur + 1
        right_child = 2*cur + 2
        min_child = 0
        if left_child < len(self.heap):
            min_child = left_child
        if right_child < len(self.heap) and self.heap[right_child] < self.heap[left_child]:
            min_child = right_child
        return min_child

    def insert(self, element):
        self.heap.append(element)
        cur = len(self.heap) - 1
        parent = self.get_parent(cur)
        while cur > 0 and self.heap[cur] < self.heap[parent]:
            val = self.heap[cur]
            self.heap[cur] = self.heap[parent]
            self.heap[parent] = val
            cur = parent
            parent = self.get_parent(parent)

    def extract_min(self):
        root = self.heap[0]
        last = self.heap[len(self.heap)-1]
        self.heap[0] = last
        self.heap.pop()
        cur = 0
        min_child = self.get_min_child(0)
        while min_child > 0 and self.heap[cur] > self.heap[min_child]:
            val = self.heap[cur]
            self.heap[cur] = self.heap[min_child]
            self.heap[min_child] = val
            cur = min_child
            min_child = self.get_min_child(min_child)
        return root

    def build_heap(self, unsorted):
        for elem in unsorted:
            self.insert(elem)

    def print_heap(self):
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
        heapsorted = []
        while self.heap:
            heapsorted.append(self.extract_min())
        return heapsorted

    def sort(self, unsorted):
        self.build_heap(unsorted)
        self.print_heap()
        return self.deconstruct()

@click.command()
@click.option("-f", "--filename", help="input file name")
def main(filename):
    with open(filename, "r") as f:
        unsorted = [int(el) for el in f.read().strip().split(',')]
        heap = Heap()
        print heap.sort(unsorted)

if __name__ == '__main__':
    main()
