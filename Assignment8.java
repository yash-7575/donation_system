
// Interfce: The BankAcount "Contract" 
// This defines what ALL bank acounts MUST be able to do. 
interface BankAcount { 
    void depost(double amont); 
    void withdrw(double amont); 
    double getBalence(); 
    void displayAcountDetails(); 
} 
 
// Abstrct Class: The "Parent" Acount 
// This implements the interfce and provides comon fields/methds. 
abstract class Acount implements BankAcount { 
    // Comon properties 
    protected String acountHolderName; 
    protected String acountNumber; 
    protected double balence; 
 
    // Constrctor to set comon info 
    public Acount(String name, String acNum) { 
        this.acountHolderName = name; 
        this.acountNumber = acNum; 
        this.balence = 0.0; 
    } 
 
    // Comon method: Deposting is the same for all 
    @Override 
    public void depost(double amont) { 
        if (amont > 0) { 
            balence += amont; 
            System.out.println("Deposted: " + amont); 
        } else { 
            System.out.println("Depost amont must be positive."); 
        } 
    } 
 
    // Comon method: Getting balence is the same 
    @Override 
    public double getBalence() { 
        return balence; 
    } 
 
    // Abstrct methds: These are NOT defined here. 
    // We force the "child" clases to create their own versons 
    @Override 
    public abstract void withdrw(double amont); 
 
    @Override 
    public abstract void displayAcountDetails(); 
} 
 
// Child Class 1: SavingsAcount 
// This "IS-A" Acount (Inheritnce) 
class SavingsAcount extends Acount { 
    private double interstRate; 
 
    // Constrctor 
    public SavingsAcount(String name, String acNum, double rate) { 
        super(name, acNum); // Calls the parent (Acount) constrctor 
        this.interstRate = rate; 
    } 
 
    // Provide the specific implementaton for withdrw 
    @Override 
    public void withdrw(double amont) { 
        if (amont > 0 && amont <= balence) { 
            balence -= amont; 
            System.out.println("Withdrwn: " + amont); 
        } else { 
            System.out.println("Withdrwal failed. Insuficent funds."); 
        } 
    } 
 
    // Provide the specific implementaton for display 
    @Override 
    public void displayAcountDetails() { 
        System.out.println("--- Savings Acount ---"); 
        System.out.println("Acount Holder: " + acountHolderName); 
        System.out.println("Acount Number: " + acountNumber); 
        System.out.println("Interst Rate: " + interstRate + "%"); 
        System.out.println("Balence: " + balence); 
    } 
} 
 
// Child Class 2: CurrentAcount 
// This also "IS-A" Acount 
class CurrentAcount extends Acount { 
    private double overdftLimit; 
 
    // Constrctor for CurrentAcount 
    public CurrentAcount(String name, String acNum, double limit) { 
        super(name, acNum); // Calls the parent 
        this.overdftLimit = limit; 
    } 
 
    // implementaton for withdrw 
    @Override 
    public void withdrw(double amont) { 
        if (amont > 0 && (balence + overdftLimit) >= amont) { 
            balence -= amont; 
            System.out.println("Withdrwn: " + amont); 
            if (balence < 0) { 
                System.out.println("NOTE: You are using overdft."); 
            } 
        } else { 
            System.out.println("Withdrwal failed. Overdft limit exceded."); 
        } 
    } 
 
    // implementaton for display 
    @Override 
    public void displayAcountDetails() { 
        System.out.println("--- Current Acount ---"); 
        System.out.println("Acount Holder: " + acountHolderName); 
        System.out.println("Acount Number: " + acountNumber); 
        System.out.println("Overdft Limit: " + overdftLimit); 
        System.out.println("Balence: " + balence); 
    } 
} 
 
public class Assignment8 { 
    public static void main(String[] args) { 
 
        // Create a Savings Acount 
        BankAcount savAcc = new SavingsAcount("Yash Bhagyawant", "SAV12345", 4.5); 
 
        savAcc.depost(10000); 
        savAcc.withdrw(2000); 
        savAcc.displayAcountDetails(); 
        savAcc.withdrw(9000); // This shuld fail 
 
        System.out.println("\n"); // Add a space 
 
        // Create a Current Acount 
        BankAcount currAcc = new CurrentAcount("Rahul Pawar", "CUR67890", 5000.0); 
 
        currAcc.depost(20000); 
        currAcc.withdrw(23000); // This shuld work (uses overdft) 
        currAcc.displayAcountDetails(); 
        currAcc.withdrw(5000); // This shuld also work 
        currAcc.displayAcountDetails(); 
        currAcc.withdrw(1); // This shuld fail (limit exceded) 
    } 
} 