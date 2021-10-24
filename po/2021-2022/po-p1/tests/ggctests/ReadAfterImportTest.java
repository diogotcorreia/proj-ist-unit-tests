package ggctests;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import ggctests.utils.PoUILibTest;

import ggc.app.exceptions.InvalidDateException;

public class ReadAfterImportTest {

    private abstract class GenericReadAfterImportTest extends PoUILibTest {

        private String testId;

        private GenericReadAfterImportTest(String testId) {
            this.testId = testId;
        }

        protected void setupWarehouseManager() {
            loadFromInputFile("test" + testId + ".input");
        }

        @Test
        void listPartners() {
            this.interaction.addMenuOptions(6, 2);

            this.runApp();

            assertEquals(getTextFromFile("expected/test" + testId + "/partners.output"), this.interaction.getResult());
        }

        @Test
        void listProducts() {
            this.interaction.addMenuOptions(5, 1);

            this.runApp();

            assertEquals(getTextFromFile("expected/test" + testId + "/products.output"), this.interaction.getResult());
        }

        @Test
        void listBatches() {
            this.interaction.addMenuOptions(5, 2);

            this.runApp();

            assertEquals(getTextFromFile("expected/test" + testId + "/batches.output"), this.interaction.getResult());
        }
    }

    @Nested
    public class ExampleInputFromWikiTest extends GenericReadAfterImportTest {
        public ExampleInputFromWikiTest() {
            super("001");
        }

        void listBatches() {}
    }

    /**
    Corresponds to test A-01-02-M-ok
     */
    @Nested
    public class InputWithOnlyPartnersTest extends GenericReadAfterImportTest {
        public InputWithOnlyPartnersTest() {
            super("002");
        }

        void listProducts() {}
        void listBatches() {}
    }

    /**
    Corresponds to test A-01-04-M-ok
     */
    @Nested
    public class InputWithPartnersAndSimpleProducts1Test extends GenericReadAfterImportTest {
        public InputWithPartnersAndSimpleProducts1Test() {
            super("003");
        }
    }

    /**
    Corresponds to test A-03-02-M-ok
     */
    @Nested
    public class InputWithPartnersAndSimpleProducts2Test extends GenericReadAfterImportTest {
        public InputWithPartnersAndSimpleProducts2Test() {
            super("004");
        }
    }

}