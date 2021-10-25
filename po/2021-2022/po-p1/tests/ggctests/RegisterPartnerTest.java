package ggctests;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import ggctests.utils.PoUILibTest;

import ggc.app.exceptions.DuplicatePartnerKeyException;

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
        protected void setupWarehouseManager() {}

        /**
        Corresponds to test A-09-01-M-ok
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

    @Nested
    public class RegisterPartnerWithExistingPartnerList extends GenericRegisterPartnerTest {
        public RegisterPartnerWithExistingPartnerList() {
            super("010");
        }

        /**
        Corresponds to test A-09-02-M-ok
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

        /**
        Corresponds to test A-09-04-M-ok
        */
        @Test
        void registerPartnersWithDuplicatedKey() {
            this.interaction.addMenuOptions(6, 3, 3, 3, 2);
            this.interaction.addFieldValues("YYYYYYYY", "wer", "rwer", "YYYYYYYY", "sdfsd", "fsd", "CCCCCCCCP1", "nome", "endere");

            this.runApp();

            assertThrownCommandException(DuplicatePartnerKeyException.class, "O parceiro 'YYYYYYYY' já existe.");
            assertThrownCommandException(DuplicatePartnerKeyException.class, "O parceiro 'CCCCCCCCP1' já existe.");
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

}
