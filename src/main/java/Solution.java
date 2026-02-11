/**
 * Example Solution class for coding exercises.
 * This file demonstrates the cheating detection system's ability to detect
 * large code pastes (velocity spikes).
 */
public class Solution {
    
    /**
     * Sorts an array using bubble sort algorithm.
     * Time complexity: O(n^2)
     * Space complexity: O(1)
     */
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap arr[j] and arr[j+1]
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    
    /**
     * Implements binary search on a sorted array.
     * Time complexity: O(log n)
     * Space complexity: O(1)
     */
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            }
            
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1; // Not found
    }
    
    /**
     * Calculates the factorial of a number recursively.
     */
    public static long factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    /**
     * Calculates the nth Fibonacci number using dynamic programming.
     */
    public static long fibonacci(int n) {
        if (n <= 1) {
            return n;
        }
        
        long[] fib = new long[n + 1];
        fib[0] = 0;
        fib[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            fib[i] = fib[i - 1] + fib[i - 2];
        }
        
        return fib[n];
    }
    
    /**
     * Checks if a string is a palindrome.
     */
    public static boolean isPalindrome(String str) {
        str = str.toLowerCase().replaceAll("[^a-z0-9]", "");
        int left = 0;
        int right = str.length() - 1;
        
        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        
        return true;
    }
    
    /**
     * Reverses a linked list.
     */
    static class ListNode {
        int val;
        ListNode next;
        
        ListNode(int val) {
            this.val = val;
        }
    }
    
    public static ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        
        while (current != null) {
            ListNode nextTemp = current.next;
            current.next = prev;
            prev = current;
            current = nextTemp;
        }
        
        return prev;
    }
    
    /**
     * Finds the maximum subarray sum using Kadane's algorithm.
     */
    public static int maxSubarraySum(int[] arr) {
        int maxSoFar = arr[0];
        int maxEndingHere = arr[0];
        
        for (int i = 1; i < arr.length; i++) {
            maxEndingHere = Math.max(arr[i], maxEndingHere + arr[i]);
            maxSoFar = Math.max(maxSoFar, maxEndingHere);
        }
        
        return maxSoFar;
    }
    
    /**
     * Performs depth-first search on a graph.
     */
    public static void dfs(int[][] graph, int node, boolean[] visited) {
        visited[node] = true;
        System.out.print(node + " ");
        
        for (int i = 0; i < graph[node].length; i++) {
            if (graph[node][i] == 1 && !visited[i]) {
                dfs(graph, i, visited);
            }
        }
    }
    
    /**
     * Calculates the greatest common divisor using Euclidean algorithm.
     */
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
    
    /**
     * Main method for testing.
     */
    public static void main(String[] args) {
        // Test bubble sort
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        bubbleSort(arr);
        System.out.println("Sorted array:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();
        
        // Test binary search
        int[] sortedArr = {2, 3, 4, 10, 40};
        int target = 10;
        int result = binarySearch(sortedArr, target);
        System.out.println("Element found at index: " + result);
        
        // Test factorial
        System.out.println("Factorial of 5: " + factorial(5));
        
        // Test Fibonacci
        System.out.println("10th Fibonacci number: " + fibonacci(10));
        
        // Test palindrome
        System.out.println("Is 'racecar' a palindrome? " + isPalindrome("racecar"));
        
        // Test max subarray sum
        int[] arr2 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("Maximum subarray sum: " + maxSubarraySum(arr2));
        
        // Test GCD
        System.out.println("GCD of 48 and 18: " + gcd(48, 18));
    }
}

    // Added a small comment
// Test change
// Another test
// Small change
