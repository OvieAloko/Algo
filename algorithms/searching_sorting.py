class SortingSearching():
    def __init__(self, is_ascending, item, list1):
        self.is_ascending = is_ascending
        self.list1 = list1
        self.item = item        

    def is_valid(self):
        if str(self.list1[0]).isnumeric():
            for i in self.list1:
                if not str(i).isnumeric():
                    return False
            else: return True
        else:
            for i in self.list1:
                if not str(i).isalpha():
                    return False
            else: return True   

    def bubble_sort(self):
        steps = []
        list2 = self.list1.copy()
        array_versions = [list2.copy()]
        compare_indices = [] 

        for i in range(len(list2)):
            changes = False
            for index in range(1, len(list2) - i):
                temp = None
                compare_indices.append((index-1, index))

                if self.is_ascending:
                    if list2[index-1] > list2[index]:
                        temp = list2[index-1]
                        list2[index-1] = list2[index]
                        list2[index] = temp
                        changes = True
                        steps.append(f"Since {list2[index-1]} is bigger than {list2[index]}, we swap them and move on to the next two numbers")
                    elif list2[index-1] < list2[index]:
                        steps.append(f"Since {list2[index-1]} is smaller than {list2[index]}, we leave the numbers and move on to the next two.")
                    else:
                        steps.append(f"Since {list2[index]} is equal to {list2[index-1]}, we leave the numbers and move on to the next two.")

                else:
                    if list2[index-1] < list2[index]:
                        steps.append(f"Since {list2[index]} is smaller than {list2[index-1]}, we swap them and move on to the next two numbers")
                        temp = list2[index-1]
                        list2[index-1] = list2[index]
                        list2[index] = temp
                        changes = True
                    elif list2[index-1] > list2[index]:
                        steps.append(f"Since {list2[index]} is larger than {list2[index-1]}, we leave the numbers and move on to the next two.")
                    else:
                        steps.append(f"Since {list2[index]} is equal to {list2[index-1]}, we leave the numbers and move on to the next two.")
                
                array_versions.append(list2.copy())
            if not changes:
                break
        return list2, steps, array_versions, compare_indices   
    
    def binary_search(self):
        steps = []
        list2 = self.list1.copy()
        array_versions = [list2.copy()]
        compare_indices = [] 

        top = len(list2)-1
        bottom = 0
        is_found = False

        list2.sort()
        steps.append("Binary search requires a sorted list, so we sort the list first.")
        array_versions.append(list2.copy())
        compare_indices.append([None, None, None])

        while not is_found and top >= bottom:
            middle = (top + bottom) // 2

            steps.append(f"We check the middle value at index {middle}, which is {list2[middle]}")
            compare_indices.append([bottom, top, middle])
            array_versions.append(list2.copy())

            if list2[middle] == self.item:
                steps.append(f"Since the middle pointer {list2[middle]} is equal to {self.item}, we have found the item at index {middle}")
                compare_indices.append([bottom, top, middle])
                array_versions.append(list2.copy())
                is_found = True

            elif list2[middle] > self.item:
                steps.append(f"Since {list2[middle]} is larger than {self.item}, we now search the left half of the list.")
                top = middle - 1
                compare_indices.append([bottom, top, None])
                array_versions.append(list2.copy())

            else:
                steps.append(f"Since {list2[middle]} is less than {self.item}, we now search the right half of the list.")
                bottom = middle + 1
                compare_indices.append([bottom, top, None])
                array_versions.append(list2.copy())



        if not is_found:
            steps.append(f"{self.item} is not in the list")
            array_versions.append(list2.copy())
            compare_indices.append([bottom, top, None])

        return is_found, steps, array_versions, compare_indices, self.item

            