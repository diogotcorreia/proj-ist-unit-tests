package ggctests;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.params.provider.CsvSource;
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

            assertNoMoreExceptions();
            assertEquals(getTextFromFile("expected/test" + testId + "/partners.output"), this.interaction.getResult());
        }

        @Test
        void listProducts() {
            this.interaction.addMenuOptions(5, 1);

            this.runApp();

            assertNoMoreExceptions();
            assertEquals(getTextFromFile("expected/test" + testId + "/products.output"), this.interaction.getResult());
        }

        @Test
        void listBatches() {
            this.interaction.addMenuOptions(5, 2);

            this.runApp();

            assertNoMoreExceptions();
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
    Corresponds to tests A-03-02-M-ok and A-04-02-M-ok
     */
    @Nested
    public class InputWithPartnersAndSimpleProducts2Test extends GenericReadAfterImportTest {
        public InputWithPartnersAndSimpleProducts2Test() {
            super("004");
        }
    }

    /**
    Corresponds to test A-03-03-M-ok
     */
    @Nested
    public class InputWithPartnersAndSimpleProducts3Test extends GenericReadAfterImportTest {
        public InputWithPartnersAndSimpleProducts3Test() {
            super("005");
        }
    }

    /**
    Corresponds to test A-04-03-M-ok
     */
    @Nested
    public class InputWithProductWithMultipleBatches1Test extends GenericReadAfterImportTest {
        public InputWithProductWithMultipleBatches1Test() {
            super("006");
        }
    }

    /**
    Corresponds to test A-04-04-M-ok
     */
    @Nested
    public class InputWithProductWithMultipleBatches2Test extends GenericReadAfterImportTest {
        public InputWithProductWithMultipleBatches2Test() {
            super("007");
        }
    }

    /**
    Corresponds to test A-07-01-M-ok
     */
    @Nested
    public class ShowPartnerByKeyTest extends GenericReadAfterImportTest {
        public ShowPartnerByKeyTest() {
            super("008");
        }

        @ParameterizedTest(name = "get partner with key {0}")
        @CsvSource(
            delimiter = ';',
            value = {
                "M1;M1|Rohit Figueiredo|New Delhi, India|NORMAL|0|0|0|0",
                "P1;P1|Lages do Chão|Lisboa, Portugal|NORMAL|0|0|0|0",
                "W2;W2|Pedraria Fonseca|Oeiras, Portugal|NORMAL|0|0|0|0"
            }
        )
        void getPartnerByKey(String key, String expectedResult) {
            this.interaction.addMenuOptions(6, 1);
            this.interaction.addFieldValues(key);

            this.runApp();

            assertNoMoreExceptions();
            assertEquals(expectedResult, this.interaction.getResult());
        }

        void listProducts() {}
        void listBatches() {}
    }

    /**
    Corresponds to test A-07-02-M-ok
     */
    @Nested
    public class PartnerKeyCaseInsensitiveTest extends GenericReadAfterImportTest {
        public PartnerKeyCaseInsensitiveTest() {
            super("009");
        }

        @ParameterizedTest
        @ValueSource(strings = { "MmMmAa1", "mmmmaa1", "mMmMaA1", "MMMMAA1" })
        void getPartnerByKey1(String partnerKey) {
            this.interaction.addMenuOptions(6, 1);
            this.interaction.addFieldValues(partnerKey);

            this.runApp();

            assertNoMoreExceptions();
            assertEquals("MmMmAa1|Rohit Figueiredo|New Delhi, India|NORMAL|0|0|0|0", this.interaction.getResult());
        }

        void listProducts() {}
        void listBatches() {}
    }

}
