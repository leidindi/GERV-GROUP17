import java.util.Arrays;

public class PriorityQueue {
    private int[] array;
    private int size;

    public PriorityQueue() {
        // Initialize the array with a default size of 10
        array = new int[10];
        size = 0;
    }

    public void add(int value) {
        // Check if the array is full and resize if necessary
        if (size == array.length) {
            array = Arrays.copyOf(array, array.length * 2);
        }

        // Add the new value to the next available spot in the array
        array[size] = value;

        // Shift the value up to its proper position in the heap
        int currentIndex = size;
        int parentIndex = (currentIndex - 1) / 2;
        while (currentIndex > 0 && array[currentIndex] > array[parentIndex]) {
            swap(currentIndex, parentIndex);
            currentIndex = parentIndex;
            parentIndex = (currentIndex - 1) / 2;
        }

        size++;
    }

    public int poll() {
        // Check if the queue is empty
        if (size == 0) {
            throw new IllegalStateException("Queue is empty");
        }

        int result = array[0];

        // Move the last element in the array to the top
        array[0] = array[size - 1];
        size--;

        // Shift the value down to its proper position in the heap
        int currentIndex = 0;
        while (currentIndex < size) {
            int leftChildIndex = 2 * currentIndex + 1;
            int rightChildIndex = 2 * currentIndex + 2;

            if (leftChildIndex >= size) {
                // The current node has no children
                break;
            } else if (rightChildIndex >= size) {
                // The current node has only a left child
                if (array[currentIndex] < array[leftChildIndex]) {
                    swap(currentIndex, leftChildIndex);
                }
                break;
            } else {
                // The current node has two children
                if (array[leftChildIndex] > array[rightChildIndex]) {
                    if (array[currentIndex] < array[leftChildIndex]) {
                        swap(currentIndex, leftChildIndex);
                        currentIndex = leftChildIndex;
                    } else {
                        break;
                    }
                } else {
                    if (array[currentIndex] < array[rightChildIndex]) {
                        swap(currentIndex, rightChildIndex);
                        currentIndex = rightChildIndex;
                    } else {
                        break;
                    }
                }
            }
        }

        return result;
    }

    public int peek() {
        // Check if the queue is empty
        if (size == 0) {
            throw new IllegalStateException("Queue is empty");
        }

        return array[0];
    }

    public boolean isEmpty() {
        return size == 0;
    }

    private void swap(int index1, int index2) {
        int temp = array[index1];
        array[index1] = array[index2];
        array[index2] = temp;
    }
}