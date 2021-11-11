package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class LookupBatchesUnderGivenPriceTest extends PoUILibTest {

    public LookupBatchesUnderGivenPriceTest() {
      super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("A-13-01-M-ok - Vê caso de warehouse sem produtos")
    void whenWarehouseHasNoProducts() {
        this.interaction.addMenuOptions(8, 1);
        this.interaction.addFieldValues("300");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-13-02-M-ok - Vê caso de warehouse com produtos sem lotes")
    void whenWarehouseHasNoBatchesButHasProducts() {
        // simulate esgotado.ggc
        loadFromInputFile("test034.input");
        this.interaction.addMenuOptions(7, 3, 0);
        this.interaction.addFieldValues("M1", "2", "SAL", "10"); // add sell transaction
        this.interaction.addMenuOptions(5, 1, 0, 8, 1);
        this.interaction.addFieldValues("4");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                HIDROGENIO|2|5000
                ROLHA|2|500
                SAL|1|0
                VIDRO|1|500
                HIDROGENIO|S1|2|5000
                ROLHA|M1|2|500
                VIDRO|M1|1|500""", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-13-03-M-ok - Vê caso de warehouse com limite superior a todos os lotes")
    void whenLimitIsAboveAllBatchPrices() {
        loadFromInputFile("test027.input");
        this.interaction.addMenuOptions(8, 1);
        this.interaction.addFieldValues("2000");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                HIDROGENIO|S1|200|5000
                ROLHA|M1|30|500
                ROLHA|R1|20|500
                SAL|S1|1000|500
                VIDRO|M1|1000|500""", this.interaction.getResult());
    }

}
