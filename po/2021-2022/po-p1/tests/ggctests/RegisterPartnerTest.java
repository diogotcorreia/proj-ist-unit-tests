package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class RegisterPartnerTest {

    private abstract class GenericRegisterPartnerTest extends PoUILibTest {

        private String testId;

        private GenericRegisterPartnerTest(String testId) {
            super(true);
            this.testId = testId;
        }

        protected void setupWarehouseManager() {
            loadFromInputFile("test" + testId + ".input");
        }
    }

    @Nested
    public class RegisterPartnerWithEmptyWarehouse extends PoUILibTest {
        protected void setupWarehouseManager() {
        }

        /**
         * Corresponds to test A-09-01-M-ok
         */
        @Test
        void registerPartner() {
            this.interaction.addMenuOptions(6, 3, 2);
            this.interaction.addFieldValues("aaa", "dwd", "ende@sfsdf-com");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals("aaa|dwd|ende@sfsdf-com|NORMAL|0|0|0|0", this.interaction.getResult());
        }
    }

    /**
     * Corresponds to test A-07-04-M-ok
     */
    @Nested
    @DisplayName("A-07-04-M-ok - Ver Parceiro não existente sem parceiros carregados e ver parceiros vazio")
    public class ReadUnknownProductAndListEmptyPartnerList extends PoUILibTest {
        protected void setupWarehouseManager() {
        }

        @ParameterizedTest(name = "trying to show partner '{0}' that does not exist")
        @ValueSource(strings = {"we", "WERT"})
        void readUnknownPartner(String key) {
            this.interaction.addMenuOptions(6, 1);
            this.interaction.addFieldValues(key);

            this.runApp();

            assertThrownCommandException("UnknownPartnerKeyException", "O parceiro '" + key + "' não existe.");
            assertNoMoreExceptions();
            assertEquals("", this.interaction.getResult());
        }

        @Test
        void listEmptyPartners() {
            this.interaction.addMenuOptions(6, 2);

            this.runApp();

            assertNoMoreExceptions();
            assertEquals("", this.interaction.getResult());
        }
    }

    @Nested
    public class RegisterPartnerWithExistingPartnerList extends GenericRegisterPartnerTest {
        public RegisterPartnerWithExistingPartnerList() {
            super("010");
        }

        /**
         * Corresponds to test A-09-02-M-ok
         */
        @Test
        void registerPartnerInTheEndOfTheList() {
            this.interaction.addMenuOptions(6, 3, 2);
            this.interaction.addFieldValues("RRRrrrrrr", "RRR", "rr@rrr");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals("""
                            AAAAS1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                            BBBBW2|Pedraria Fonseca|Oeiras, Portugal|NORMAL|0|0|0|0
                            CCCCCCCCP1|Lages do Chão|Lisboa, Portugal|NORMAL|0|0|0|0
                            DDDDDDP3|ObBrian Rocks|Koln, Germany|NORMAL|0|0|0|0
                            EEEEEER2|Jorge Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            EFFFFF4|Filomena Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            RRRrrrrrr|RRR|rr@rrr|NORMAL|0|0|0|0""",
                    this.interaction.getResult());
        }

        @Test
        void registerPartnerInVariousPositionsOfTheList() {
            this.interaction.addMenuOptions(6, 3, 3, 3, 2);
            this.interaction.addFieldValues("AAAAAPrimeiro", "primeiro", "prim@iro", "CCCEE", "cee", "cee@cee", "DDO", "dodot", "do@dot");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals("""
                            AAAAAPrimeiro|primeiro|prim@iro|NORMAL|0|0|0|0
                            AAAAS1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                            BBBBW2|Pedraria Fonseca|Oeiras, Portugal|NORMAL|0|0|0|0
                            CCCCCCCCP1|Lages do Chão|Lisboa, Portugal|NORMAL|0|0|0|0
                            CCCEE|cee|cee@cee|NORMAL|0|0|0|0
                            DDDDDDP3|ObBrian Rocks|Koln, Germany|NORMAL|0|0|0|0
                            DDO|dodot|do@dot|NORMAL|0|0|0|0
                            EEEEEER2|Jorge Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            EFFFFF4|Filomena Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0""",
                    this.interaction.getResult());
        }

        /**
         * Corresponds to test A-09-04-M-ok
         */
        @Test
        void registerPartnersWithDuplicatedKey() {
            this.interaction.addMenuOptions(6, 3, 3, 3, 2);
            this.interaction.addFieldValues("YYYYYYYY", "wer", "rwer", "YYYYYYYY", "sdfsd", "fsd", "CCCCCCCCP1", "nome", "endere");

            this.runApp();

            assertThrownCommandException("DuplicatePartnerKeyException", "O parceiro 'YYYYYYYY' já existe.");
            assertThrownCommandException("DuplicatePartnerKeyException", "O parceiro 'CCCCCCCCP1' já existe.");
            assertNoMoreExceptions();
            assertEquals("""
                            AAAAS1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                            BBBBW2|Pedraria Fonseca|Oeiras, Portugal|NORMAL|0|0|0|0
                            CCCCCCCCP1|Lages do Chão|Lisboa, Portugal|NORMAL|0|0|0|0
                            DDDDDDP3|ObBrian Rocks|Koln, Germany|NORMAL|0|0|0|0
                            EEEEEER2|Jorge Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            EFFFFF4|Filomena Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            YYYYYYYY|wer|rwer|NORMAL|0|0|0|0""",
                    this.interaction.getResult());
        }
    }

    @Nested
    public class RegisterDuplicatePartnerWithExistingPartnerList extends GenericRegisterPartnerTest {
        public RegisterDuplicatePartnerWithExistingPartnerList() {
            super("023");
        }

        /**
         * Corresponds to test A-09-05-M-ok
         */
        @Test
        @DisplayName("A-09-05-M-ok - Registar parceiro com chave diferente mas duplicada")
        void registerPartnersWithDuplicatedKey() {
            this.interaction.addMenuOptions(6, 3, 3, 3, 3, 2);
            this.interaction.addFieldValues("aaAAS1", "we", "we", "ddddddp3", "we", "we", "WEWE", "nos", "nos", "WewE", "nos 2", "nos 2");

            this.runApp();

            assertThrownCommandException("DuplicatePartnerKeyException", "O parceiro 'aaAAS1' já existe.");
            assertThrownCommandException("DuplicatePartnerKeyException", "O parceiro 'ddddddp3' já existe.");
            assertThrownCommandException("DuplicatePartnerKeyException", "O parceiro 'WEWE' já existe.");
            assertThrownCommandException("DuplicatePartnerKeyException", "O parceiro 'WewE' já existe.");
            assertNoMoreExceptions();
            assertEquals("""
                            AAAAS1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                            BBBBW2|Pedraria Fonseca|Oeiras, Portugal|NORMAL|0|0|0|0
                            CCCCCCCCP1|Lages do Chão|Lisboa, Portugal|NORMAL|0|0|0|0
                            DDDDDDP3|ObBrian Rocks|Koln, Germany|NORMAL|0|0|0|0
                            EEEEEER2|Jorge Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            EFFFFF4|Filomena Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            wewe|Cristiano Ronaldo|Lisboa, Portugal|NORMAL|0|0|0|0""",
                    this.interaction.getResult());
        }
    }

    @Nested
    public class RegisterMixedCasePartnersInExistingPartnerList extends GenericRegisterPartnerTest {
        public RegisterMixedCasePartnersInExistingPartnerList() {
            super("024");
        }

        /**
         * Corresponds to test A-09-06-M-ok
         */
        @Test
        @DisplayName("A-09-06-M-ok - Registar parceiro com chave minusculas/maiúsculas no meio e ver que está bem ordenado")
        void registerPartnersWithDuplicatedKey() {
            this.interaction.addMenuOptions(6, 3, 3, 3, 3, 2);
            this.interaction.addFieldValues("aaaaaaaaaaaaa", "aa", "aa", "dede", "de de", "de@de", "eeEE", "ee EE", "e@e", "yyy", "yyy", "yyyyyy");

            this.runApp();

            assertNoMoreExceptions();
            assertEquals("""
                            aaaaaaaaaaaaa|aa|aa|NORMAL|0|0|0|0
                            AAAAS1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                            BBBBW2|Pedraria Fonseca|Oeiras, Portugal|NORMAL|0|0|0|0
                            CON|Lages do Chão-con|Lisboa, Portugal|NORMAL|0|0|0|0
                            DDDDDDP3|ObBrian Rocks|Koln, Germany|NORMAL|0|0|0|0
                            dede|de de|de@de|NORMAL|0|0|0|0
                            eeEE|ee EE|e@e|NORMAL|0|0|0|0
                            EEEEEER2|Jorge Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            EFFFFF4|Filomena Figueiredo|Lisboa, Portugal|NORMAL|0|0|0|0
                            yyy|yyy|yyyyyy|NORMAL|0|0|0|0""",
                    this.interaction.getResult());
        }
    }

}
