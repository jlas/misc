// Print back to back triangles
public class Triangle {

    public static final int ROWS = 10;
    public static final int COLS = ROWS-1;

    public static void main(String[] args) {
        for (int i = 0; i < ROWS; i++) {

            // Left triangle
            for (int j = 0; j < COLS; j++) {
                if (   j == i
                    || j == 0
                    || i == ROWS-1) {
                    System.out.print("*");
                } else {
                    System.out.print(" ");
                }
            }

            // Right traingle
            for (int j = COLS; j >= 0; j--) {
                if (   j == i
                    || j == 0
                    || i == ROWS-1) {
                    System.out.print("*");
                } else {
                    System.out.print(" ");
                }
            }

            System.out.println();
        }
    }
}
