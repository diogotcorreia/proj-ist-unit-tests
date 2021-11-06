package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;

import java.io.File;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class LoadAndSaveTest extends PoUILibTest {

    protected void setupWarehouseManager() {
    }

    @TestMethodOrder(MethodOrderer.OrderAnnotation.class)
    private abstract class GenericLoadAndSaveTest extends PoUILibTest {

        protected String testId;

        private GenericLoadAndSaveTest(String testId) {
            this.testId = testId;
        }

        protected void setupWarehouseManager() {
            loadFromInputFile("test" + testId + ".input");
        }

        protected void assertFileExists(String fileName) {
            assertTrue(new File(fileName).exists(), "File " + fileName + " was not created");
        }

        protected void cleanUpFile(String fileName) {
            new File(fileName).delete();
        }

        protected void resetWarehouseManager() {
            this.warehouseManager = newWarehouseManager();
        }
    }

    /**
     * Corresponds to test A-01-02-M-ok/A-01-03-M-ok
     */
    @Nested
    public class LoadAndSavePartnersTest extends GenericLoadAndSaveTest {
        private LoadAndSavePartnersTest() {
            super("002");
        }

        @Test
        @Order(1)
        void saveFile() {
            this.interaction.addMenuOptions(2);
            this.interaction.addFieldValues("app01.dat");

            this.runApp();

            assertNoMoreExceptions();
            assertFileExists("app01.dat");
            assertEquals("", this.interaction.getResult());
        }


        @Test
        @Order(2)
        void loadFile() {
            this.resetWarehouseManager();
            this.interaction.addMenuOptions(1, 6, 2);
            this.interaction.addFieldValues("app01.dat");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals(getTextFromFile("expected/test" + testId + "/partners.output"), this.interaction.getResult());
        }

        @AfterAll
        void cleanUpFiles() {
            cleanUpFile("app01.dat");
        }

    }

    /**
     * Corresponds to test A-01-04-M-ok/A-01-05-M-ok
     */
    @Nested
    public class LoadAndSavePartnersAndSimpleProductsTest extends GenericLoadAndSaveTest {
        private LoadAndSavePartnersAndSimpleProductsTest() {
            super("003");
        }

        @Test
        @Order(1)
        void saveFile() {
            this.interaction.addMenuOptions(2);
            this.interaction.addFieldValues("app02.dat");

            this.runApp();

            assertNoMoreExceptions();
            assertFileExists("app02.dat");
            assertEquals("", this.interaction.getResult());
        }


        @Test
        @Order(2)
        void loadFile() {
            this.resetWarehouseManager();
            this.interaction.addMenuOptions(1, 5, 1, 0, 6, 2);
            this.interaction.addFieldValues("app02.dat");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals(getTextFromFile("expected/test" + testId + "/products.output") + "\n" +
                    getTextFromFile("expected/test" + testId + "/partners.output"), this.interaction.getResult());
        }

        @AfterAll
        void cleanUpFiles() {
            cleanUpFile("app02.dat");
        }

    }

    /**
     * Corresponds to test A-01-07-M-ok/A-01-08-M-ok/A-01-09-M-ok
     */
    @Nested
    public class LoadAndSaveAddPartnerChangeDateTest extends GenericLoadAndSaveTest {
        private LoadAndSaveAddPartnerChangeDateTest() {
            super("011");
        }

        @Test
        @Order(1)
        void saveFile() {
            this.interaction.addMenuOptions(2, 6, 3, 0, 6, 2, 0, 2);
            this.interaction.addFieldValues("app03.dat", "XXXXXXXXXXXXXXXXXX", "nome", "endere");

            this.runApp();

            assertNoMoreExceptions();
            assertFileExists("app03.dat");
            assertEquals(getTextFromFile("expected/test" + testId + "/partners.output"), this.interaction.getResult());
        }


        @Test
        @Order(2)
        void loadFileChangeDateAndSaveFile() {
            this.resetWarehouseManager();
            this.interaction.addMenuOptions(1, 6, 2, 0, 4, 2);
            this.interaction.addFieldValues("app03.dat", "20");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals(getTextFromFile("expected/test" + testId + "/partners.output"), this.interaction.getResult());
        }

        @Test
        @Order(3)
        void loadFile() {
            this.resetWarehouseManager();
            this.interaction.addMenuOptions(1, 3);
            this.interaction.addFieldValues("app03.dat");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals("Data actual: 20", this.interaction.getResult());
        }

        @AfterAll
        void cleanUpFiles() {
            cleanUpFile("app03.dat");
        }

    }

    /**
     * Corresponds to test A-01-06-M-ok
     */
    @Test
    void loadFileThatDoesNotExistTest() {
        this.interaction.addMenuOptions(1);
        this.interaction.addFieldValues("file_that_does_not_exist.dat");

        this.runApp();

        assertThrownCommandException("FileOpenFailedException", "Problema ao abrir 'file_that_does_not_exist.dat'.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    /**
     * Test saving and loading derived products, including nested derived products
     */
    @Nested
    public class LoadAndSaveDerivedProductsTest extends GenericLoadAndSaveTest {
        private LoadAndSaveDerivedProductsTest() {
            super("013");
        }

        @Test
        @Order(1)
        void saveFile() {
            this.interaction.addMenuOptions(2);
            this.interaction.addFieldValues("app_test013.dat");

            this.runApp();

            assertNoMoreExceptions();
            assertFileExists("app_test013.dat");
            assertEquals("", this.interaction.getResult());
        }


        @Test
        @Order(2)
        void loadFile() {
            this.resetWarehouseManager();
            this.interaction.addMenuOptions(1, 5, 1, 0, 6, 2, 0, 5, 2);
            this.interaction.addFieldValues("app_test013.dat");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals(getTextFromFile("expected/test" + testId + "/products.output") + "\n" +
                    getTextFromFile("expected/test" + testId + "/partners.output") + "\n" +
                    getTextFromFile("expected/test" + testId + "/batches.output"), this.interaction.getResult());
        }

        @AfterAll
        void cleanUpFiles() {
            cleanUpFile("app_test013.dat");
        }

    }

}
