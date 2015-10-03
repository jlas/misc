#include <stdio.h>

/**
 * Quicksort
 */

void swap (int arr[], int aIdx, int bIdx) {
  int tmp = arr[aIdx];
  arr[aIdx] = arr[bIdx];
  arr[bIdx] = tmp;
}

void printarr(int arr[], int size) {
  int i;
  printf("size: %d\n", size);
  for (i = 0; i < size; i++) {
    printf("%d ", arr[i]);
  }
}

int partition(int arr[], int left, int right, int pivotIdx) {
  int pivotVal = arr[pivotIdx];
  int storeIdx = left;
  int i;
  swap(arr, pivotIdx, right);
  for (i=left; i < right; i++) {
    if (arr[i] <= pivotVal) {
      swap(arr, i, storeIdx);
      storeIdx += 1;
    }
  }
  swap(arr, storeIdx, right);
  return storeIdx;
}

int * quicksort(int arr[], int left, int right) {
  int pivotIdx, pivotNewIdx;
  if (left < right) {
    pivotIdx = left + ((right - left) / 2);
    pivotNewIdx = partition(arr, left, right, pivotIdx);
    quicksort(arr, left, pivotNewIdx - 1);
    quicksort(arr, pivotNewIdx + 1, right);
  }
  return arr;
}

/**
 * Selection sort
 */

int * selection(int arr[], int size) {
  int i, j, minIdx, tmp;
  for (i = 0; i < size - 1; i++) {

    /* init smallest val found to i */
    minIdx = i;
    for (j = i; j < size; j++) {

      /* found a smaller value */
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
      }
    }

    /* swap */
    tmp = arr[i];
    arr[i] = arr[minIdx];
    arr[minIdx] = tmp;
  }

  return arr;
}

/**
 * Merge sort
 */

void copyArr(int * arrFrom, int start, int end, int * arrTo) {
  int i;
  for (i = start; i < end; i++)
    arrTo[i] = arrFrom[i];
}

void topDownMerge(int * arr, int iBegin, int iMiddle, int iEnd, int * aux) {
  int i0 = iBegin;
  int i1 = iMiddle;

  int j;
  for (j = iBegin; j < iEnd; j++) {
    if (i0 < iMiddle && (i1 >= iEnd || arr[i0] <= arr[i1])) {
      aux[j] = arr[i0++];
    } else {
      aux[j] = arr[i1++];
    }
  }
}

void topDownSplitMerge(int * arr, int iBegin, int iEnd, int * aux) {
  int iMiddle;
  if (iEnd - iBegin < 2) {
    return;
  }
  iMiddle = (iEnd + iBegin) / 2;
  topDownSplitMerge(arr, iBegin, iMiddle, aux);
  topDownSplitMerge(arr, iMiddle, iEnd, aux);
  topDownMerge(arr, iBegin, iMiddle, iEnd, aux);
  copyArr(aux, iBegin, iEnd, arr);
}

void topDownMergeSort(int * arr, int * aux, int size) {
  topDownSplitMerge(arr, 0, size, aux);
}

int main (int argc, char* argv []) {
  int arr[] = { 4, 5, 10, 1, 0, 3, 28, 52, 13};
  int size = sizeof(arr)/sizeof(int);
  int aux[size];

  printf("quicksort\n");
  quicksort(arr, 0, size - 1);
  printarr(arr, size);
  printf("\n");

  printf("mergesort\n");
  topDownMergeSort(arr, aux, size);
  printarr(arr, size);
  printf("\n");
  return 0;
}
