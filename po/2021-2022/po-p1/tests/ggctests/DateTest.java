package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class DateTest extends PoUILibTest {

    protected void setupWarehouseManager() {
    }

    /**
     * Corresponds to test A-02-01-M-ok
     */
    @Test
    void displayDefaultDate() {
        this.interaction.addMenuOptions(3);

        this.runApp();

        assertEquals("Data actual: 0", this.interaction.getResult());
    }

    /**
     * Corresponds to tests A-02-02-M-ok and A-02-04-M-ok
     */
    @Test
    void changeDateAndDisplayNewDate() {
        this.interaction.addMenuOptions(4, 3, 4, 3);
        this.interaction.addFieldValues("6", "30");

        this.runApp();

        assertEquals("Data actual: 6\nData actual: 36", this.interaction.getResult());
    }

    /**
     * Corresponds to test A-02-03-M-ok
     */
    @ParameterizedTest(name = "trying to advance by {0} days")
    @ValueSource(ints = {-1, -30, 0})
    void invalidDateError(int value) {
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues(Integer.toString(value));

        this.runApp();

        assertThrownCommandException("InvalidDateException", "Data inválida: " + value);
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

}