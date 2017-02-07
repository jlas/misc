#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <time.h>

int search(int * arr, int sz, int target) {
  int start = 0;
  int end = sz;

  while (end > start) {
    int mid = start + (end - start) / 2;
    int midval = arr[mid];
    if (midval == target) {
      return mid;
    }

    if (arr[start] < arr[end-1]) {
      // sitation b, we are in a monotonically increasing slice
      if (midval < target) {
        start = mid + 1;
      } else {
        end = mid;
      }

    } else {

      // situation a-1, midpoint is on higher subsequence and target is greater
      // than mid val or less than start val
      int a1 = (midval > arr[start] &&
                (target > midval || target < arr[start]));

      // situation a-2, midpoint is on lower subsequence and target is greater
      // than mid val but less than end val
      int a2 = (midval < arr[start] &&
                (target > midval && target < arr[start]));

      if (a1 || a2) {
        start = mid + 1;
      } else {
        end = mid;
      }
    }
  }
  return -1;
}

int compare (const void* a, const void* b) {
  int a1 = *(const int *)a;
  int b1 = *(const int *)b;
  if (a1 < b1) {
    return -1;
  } else if (a1 == b1) {
    return 0;
  } else {
    return 1;
  }
}

void test(int shift, int sz) {
  int arr[sz];
  int tmp[shift];
  int i, j;

  // initialize random array
  srand(time(NULL));
  for (i = 0; i < sz; i++) {
    arr[i] = rand();
  }
  qsort(arr, sz, sizeof(int), compare);

  // shift array
  for (i = sz - shift, j =  0; i < sz; i++, j++) {
    tmp[j] = arr[i];
  }

  for (i = sz; i >= shift; i--) {
    arr[i] = arr[i-shift];
  }

  for (i = 0; i < shift; i++) {
    arr[i] = tmp[i];
  }

  // test
  for (i=0; i < sz; i++) {
    assert(i == search(arr, sz, arr[i]));
  }
}

int main() {
  int sz = 10000;
  int i, shift;

  srand(time(NULL));

  for (i = 0; i < 200; i++) {
    shift = rand() % sz;
    test(shift, sz);
  }
  return 0;
}
