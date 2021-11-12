package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class LookupPaymentsByPartnerTest extends PoUILibTest {

    public LookupPaymentsByPartnerTest() {
      super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("A-14-01-M-ok - Mostrar parceiro não existente e parceiros sem transacções")
    void showUnknownPartnerAndEmptyPartner() {
        loadFromInputFile("test027.input");
        this.interaction.addMenuOptions(8, 2, 2);
        this.interaction.addFieldValues("nãoexiste", "M1");

        this.runApp();

        assertThrownCommandException("UnknownPartnerKeyException", "O parceiro 'nãoexiste' não existe.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-14-02-M-ok - Mostrar parceiro só com compras")
    void showPartnerWithAcquisitionsOnly() {
        loadFromInputFile("test027.input");
        this.interaction.addMenuOptions(7, 4, 4, 0, 7, 1, 0);
        this.interaction.addFieldValues("M1", "SAL", "10", "10", "M1", "VIDRO", "10", "20", "0");
        this.interaction.addMenuOptions(8, 2);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("COMPRA|0|M1|SAL|10|100|0", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-14-03-M-ok - Mostrar parceiro só com vendas não pagas")
    void showPartnerWithOnlyUnpaidSales() {
        loadFromInputFile("test027.input");
        this.interaction.addMenuOptions(7, 3, 3, 0);
        this.interaction.addFieldValues("M1", "10", "ROLHA", "10", "M1", "5", "VIDRO", "25");
        this.interaction.addMenuOptions(8, 2);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("Show partner with paid sales")
    void showPartnerWithPaidSales() {
        loadFromInputFile("test027.input");
        this.interaction.addMenuOptions(7, 3, 3, 5, 0);
        this.interaction.addFieldValues("M1", "10", "ROLHA", "10", "M1", "5", "VIDRO", "25", "1");
        this.interaction.addMenuOptions(8, 2);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("VENDA|1|M1|VIDRO|25|25000|22500|5|0", this.interaction.getResult());
    }

}
