package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PartnerStatusTest extends PoUILibTest{

    public PartnerStatusTest()
    {
        super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("Parceiro sobe para Selection e ver parceiro")
    void upgradeParterStatusSelection() {
        super.loadFromInputFile("test041.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(1);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                VENDA|0|M1|HIDROGENIO|2|400|360|10|0
                M1|Rohit Figueiredo|New Delhi, India|SELECTION|4000|0|360|360""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Parceiro sobe de Selection para Elite e ver parceiro")
    void upgradeParterStatusSelectiontoELite() {
        super.loadFromInputFile("test041.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(3);
        this.interaction.addFieldValues("M1","10", "SAL", "10");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("1");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
        M1|Rohit Figueiredo|New Delhi, India|ELITE|104000|0|9360|9360""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Parceiro Elite passa para Selection e ver parceiro")
    void upgradeParterStatusELitetoSelection() {
        super.loadFromInputFile("test041.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(3);
        this.interaction.addFieldValues("M1","10", "SAL", "10");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("1");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");
        this.interaction.addMenuOptions(0, 7, 3);
        this.interaction.addFieldValues("M1","10", "VIDRO", "5");
        this.interaction.addMenuOptions(0, 4);
        this.interaction.addFieldValues("69");
        this.interaction.addMenuOptions(3,7,1);
        this.interaction.addFieldValues("2");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("2");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
        M1|Rohit Figueiredo|New Delhi, India|ELITE|104000|0|9360|9360
        Data actual: 69
        VENDA|2|M1|VIDRO|5|5000|5000|10
        M1|Rohit Figueiredo|New Delhi, India|SELECTION|26000|0|14360|14360""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Parceiro sobe para Selection e desce para Normal, ver parceiro")
    void upgradePartnerdAndDowngrade() {
        super.loadFromInputFile("test041.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(0, 4);
        this.interaction.addFieldValues("234");
        this.interaction.addMenuOptions(7, 5);
        this.interaction.addFieldValues("1");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                M1|Rohit Figueiredo|New Delhi, India|NORMAL|4000|0|5240|5240""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Parceiro sobe de Normal para Elite e ver parceiro")
    void partnerStatusNormalToElite() {
        super.loadFromInputFile("test041.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "50");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
        M1|Rohit Figueiredo|New Delhi, India|ELITE|100000|0|9000|9000""", this.interaction.getResult());
    }

    
}
