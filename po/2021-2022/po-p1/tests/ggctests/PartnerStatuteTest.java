package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PartnerStatuteTest extends PoUILibTest{

    public PartnerStatuteTest() {
        super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("Partner upgrade to SELECTION and see partner")
    void upgradePartnerStatuteSelection() {
        super.loadFromInputFile("test039.input");
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
                M1|Rohit Figueiredo|New Delhi, India|SELECTION|3600|0|400|360""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner upgrade from SELECTION to ELITE and see partner")
    void upgradePartnerStatuteSelectionToELite() {
        super.loadFromInputFile("test039.input");
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
        assertEquals("M1|Rohit Figueiredo|New Delhi, India|ELITE|93600|0|10400|9360", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner downgrade from ELITE to SELECTION and see partner")
    void downgradePartnerStatuteEliteToSelection() {
        super.loadFromInputFile("test039.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1", "10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(3);
        this.interaction.addFieldValues("M1", "10", "SAL", "10");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("1");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");
        this.interaction.addMenuOptions(0, 7, 3);
        this.interaction.addFieldValues("M1", "10", "VIDRO", "5");
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
                M1|Rohit Figueiredo|New Delhi, India|ELITE|93600|0|10400|9360
                Data actual: 69
                VENDA|2|M1|VIDRO|5|5000|5000|10
                M1|Rohit Figueiredo|New Delhi, India|SELECTION|23400|0|15400|14360""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner upgrade to SELECTION and downgrade to NORMAL, see partner")
    void upgradePartnerToSelectionAndDowngrade() {
        super.loadFromInputFile("test039.input");
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
        assertEquals("M1|Rohit Figueiredo|New Delhi, India|NORMAL|360|0|800|5240", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner upgrade from NORMAL to ELITE, see partner")
    void partnerStatuteNormalToElite() {
        super.loadFromInputFile("test039.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "50");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(0, 6, 1);
        this.interaction.addFieldValues("M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("M1|Rohit Figueiredo|New Delhi, India|ELITE|90000|0|10000|9000", this.interaction.getResult());
    }


}
