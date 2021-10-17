package ggctests;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import ggctests.utils.PoUILibTest;

import ggc.app.exceptions.InvalidDateException;

public class DateTest extends PoUILibTest {

    protected void setupWarehouseManager() {
    }

    @Test
    void displayDefaultDate() {
        this.interaction.addMenuOptions(3);

        this.runApp();

        assertEquals("Data actual: 0", this.interaction.getResult());
    }

    @Test
    void changeDateAndDisplayNewDate() {
        this.interaction.addMenuOptions(4, 3, 4, 3);
        this.interaction.addFieldValues("6", "30");

        this.runApp();

        assertEquals("Data actual: 6\nData actual: 36", this.interaction.getResult());
    }

    @Test
    void invalidDateError() {
        this.interaction.addMenuOptions(4, 4, 4);
        this.interaction.addFieldValues("-1", "-30", "0");

        this.runApp();

        assertThrownCommandException(InvalidDateException.class, "Data inválida: -1");
        assertThrownCommandException(InvalidDateException.class, "Data inválida: -30");
        assertThrownCommandException(InvalidDateException.class, "Data inválida: 0");
        assertEquals("", this.interaction.getResult());
    }

}