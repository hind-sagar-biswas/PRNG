import java.util.Random;

public class Rand {
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java RandomFloats n");
            System.exit(1);
        }
        int n = Integer.parseInt(args[0]);
        Random random = new Random();
        for (int i = 0; i < n; i++) {
            System.out.print(random.nextFloat() + " ");
        }
        System.out.println();
    }
}
