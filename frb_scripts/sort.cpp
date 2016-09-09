// MPI Quicksort, still workin on it
#include<iostream>
#include<math.h>
#include<sys/time.h>
#include<mpi.h>
#include<stdlib.h>

void swap(double *data, int i, int j) {
    int temp = data[i];
    data[i] = data[j];
    data[j] = temp;
}

int partition(double *data,int start, int end) {
    if (start>=end) {
        return 0;
    }

    int pivotValue = data[start];
    int low = start;
    int high = end -1;

    while (low<high) {
        while(data[low] <= pivotValue && low < end) {
            low++;
        }
        while (data[high] > pivotValue && high > start) {
            high--;
        }
        if (low < high) {
            swap(data, low, high);
        }
    }

    swap(data, start, high);

    return high;
}

void quicksort(double *data, int start, int end) {
    if (end-start+1 <2) {
        return;
    }

    int pivot = partition(data, start, end);

    quicksort(data, start, pivot);
    quicksort(data, pivot+1, end);
}

void randomData(double *data,int length, int size, int rank) {
    for (int i=0; i<length/size; i++) {
        // generate random float number
        data[i] = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    }

    // send back to processor 0
    MPI_Status status;
    if (rank == 0) {
        for (int i=1; i<size; i++) {
            MPI_Recv(data+i*length/size, length/size, MPI_DOUBLE, i, MPI_ANY_TAG,
                    MPI_COMM_WORLD, &status);
        }
    } else {
        MPI_Send(data, length/size, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
        delete[] data;
    }
}

void parallel_sort(double *data, int length, int size, int rank) {

}
int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);
    int rank, size, length;
    double *data;
    timeval start, end;

    MPI_Comm_rank (MPI_COMM_WORLD, &rank);
    MPI_Comm_size (MPI_COMM_WORLD, &size);
    length = pow(62,4);
    if (rank == 0 || size==1) {
        data = new double[length];
    } else {
        data = new double[length/(size-1)];
    }
    gettimeofday(&start, 0);
    randomData(data,length,size,rank);
    std::cout << sizeof(*data)/sizeof(double);
    gettimeofday(&end, 0);
    MPI_Finalize();
    }
