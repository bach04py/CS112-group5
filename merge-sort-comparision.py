import multiprocessing
import time
import numpy as np
import matplotlib.pyplot as plt

def merge(left, right): # hàm trộn hai mảng left và right
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]: # đưa phần tử nhỏ hơn trong 2 mảng vào trong mảng kết quả
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:]) # đưa tất cả phần tử còn lại trong 2 mảng vào mảng kết quả
    result.extend(right[j:])

    return result # trả lại kết quả

def MergeSort(arr): # hàm thực hiện sắp xếp trộn
    if len(arr) <= 1: # nếu độ dài dãy là 1 thì trả lại dãy
        return arr

    mid = len(arr) // 2 # lấy index ở giữa

    left = MergeSort(arr[:mid]) # gọi đệ quy merge sort cho 2 phần trái và phải
    right = MergeSort(arr[mid:])

    return merge(left, right) # trả lại mảng đã được sắp xếp trộn 2 phần left và right

def ParallelMergeSort(arr, numCore): # hàm thực hiện thuật toán merge sort song song với numCore là số bộ xử lý
    if len(arr) <= 1:
        return arr

    chunks = []
    div, mod = divmod(len(arr), numCore)
    remain = 0
    id = 0
    while id < len(arr): # làm một vòng lặp lấy vị trí
        remain = 0
        if mod > 0:
            remain = 1
            mod -= 1
        chunks.append(arr[id:id + div + remain]) # chunks[i] lưu lại các phần tử trong dãy thứ i
        id += div + remain
        
    with multiprocessing.Pool(processes=numCore) as pool:
        sorted_chunks = pool.map(MergeSort, chunks) # thực hiện sắp xếp trộn cho từng bộ xử lý thông qua phương thức pool

        while len(sorted_chunks) > 1: # khi vẫn còn chunk chưa xử lý
            next_chunks = []
            for i in range(0, len(sorted_chunks), 2): # xét từng dãy thứ i đã được sắp xếp, sắp xếp lại 2 dãy i và i + 1 bằng phương pháp trộn
                if i + 1 < len(sorted_chunks):
                    next_chunks.append(merge(sorted_chunks[i], sorted_chunks[i + 1]))
                else:
                    next_chunks.append(sorted_chunks[i])
            sorted_chunks = next_chunks

        return sorted_chunks[0] # trả lại kết quả cuối cùng

def RunningTime(func, arr, numCore): # hàm tính toán thời gian chạy của hàm func với một dãy
    start = time.time() # thời gian bắt đầu
    if numCore != -1: # nếu numCore khác -1 thì thực hiện merge sort song song
        func(arr, numCore)
    else: # ngược lại thực hiện merge sort tuần từ
        func(arr)
    end = time.time() # thời gian kết thúc
    return end - start # tổng thời gian thực hiện

if __name__ == '__main__':
    value = 1
    nSize = []
    for i in range(1, 6):
      value *= 10
      nSize.append(value)
      nSize.append(value * 5)
    core = [-1, 2, 5, 8, 10] # khởi tạo các core
    stoTime = [[] for _ in core] # lấy một mảng lưu thời gian ứng với core[i]
    for i in range(len(nSize)):
        n = nSize[i]
        arr = []
        for i in range(n):
            arr.append(np.random.randint(0, 1000001)) # bỏ random giá trị vào mảng
        for i in range(len(core)):
            if core[i] != -1: # nếu số core khác -1 thì thực hiện merge sort parallel
                stoTime[i].append(RunningTime(ParallelMergeSort, arr, core[i]))
            else: # ngược lại làm merge sort tuần tự
                stoTime[i].append(RunningTime(MergeSort, arr, core[i]))
        
        for i in range(len(core)):
            print(core[i], ":", stoTime[i][-1])
    for i in range(len(core)):
      if core[i] == -1:
        label = 'Sequential'
      else:
        label = str(core[i]) + ' core'
      plt.plot(nSize, stoTime[i], label=label)
      plt.legend(loc='lower right')
    
    plt.xlabel("Size of testcase (n)")
    plt.ylabel("Running time (s)")
    plt.show()