public class SumOfFirst1000Primes {
    public static void main(String[] args) {
        int count = 0;
        long number = 2; // Start with the first prime number
        long sum = 0;

        while (count < 1000) {
            if (isPrime(number)) {
                sum += number;
                count++;
            }
            number++;
        }

        System.out.println("Sum of the first 1000 prime numbers: " + sum);
    }

    // Function to check if a number is prime
    public static boolean isPrime(long num) {
        if (num <= 1) {
            return false;
        }
        for (long i = 2; i * i <= num; i++) {
            if (num % i == 0) {
                return false;
            }
        }
        return true;
    }
}