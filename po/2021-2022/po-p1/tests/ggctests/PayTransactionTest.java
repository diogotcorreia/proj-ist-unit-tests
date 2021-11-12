package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PayTransactionTest extends PoUILibTest {

    public PayTransactionTest() {
        super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("A-16-01-M-ok - Pagar transacção não existente")
    void payNonExistingTransaction() {
        loadFromInputFile("test041.input");
        this.interaction.addMenuOptions(7, 3, 5, 5);
        this.interaction.addFieldValues("S1", "4", "SAL", "1", "-1", "2");

        this.runApp();

        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '-1' não existe.");
        assertThrownCommandException("UnknownTransactionKeyException", "A transacção '2' não existe.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-16-02-M-ok - Pagar venda não paga (dentro do prazo)")
    void payUnpaidSaleBeforeDeadline() {
        loadFromInputFile("test041.input");
        this.interaction.addMenuOptions(7, 3, 0);
        this.interaction.addFieldValues("S1", "10", "SAL", "5");
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("9"); // advance date
        this.interaction.addMenuOptions(7, 1, 5, 1, 0);
        this.interaction.addFieldValues("0", "0", "0"); // view and pay sale
        this.interaction.addMenuOptions(6, 1);
        this.interaction.addFieldValues("S1"); // view partner

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                VENDA|0|S1|SAL|5|25|25|10
                VENDA|0|S1|SAL|5|25|25|10|9
                S1|Toshiba|Tokyo, Japan|NORMAL|250|0|25|25""", this.interaction.getResult());
    }

}
