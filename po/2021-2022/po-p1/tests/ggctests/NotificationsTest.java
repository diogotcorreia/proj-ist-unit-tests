package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class NotificationsTest extends PoUILibTest {

    public NotificationsTest() {
        super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("A-10-01-M-ok - Adiciono um batch com um preço mais alto do que alguns batches e não há notificação")
    void addBatchWithHigherPriceAndExpectNoNotifications() {
        super.loadFromInputFile("test032.input");
        this.interaction.addMenuOptions(7, 4);
        this.interaction.addFieldValues("M1", "HIDROGENIO", "500", "10");
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("M1", "SAL", "4000", "23");
        this.interaction.addMenuOptions(0, 6, 1, 1);
        this.interaction.addFieldValues("S1", "M1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                M1|Rohit Figueiredo|New Delhi, India|NORMAL|0|97000|0|0""", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-10-02-M-ok - Liga/desliga notificação de produto e parceiro não existente")
    void toggleProductNotificationsForNonUnknownProductAndPartner() {
        super.loadFromInputFile("test032.input");
        this.interaction.addMenuOptions(6, 4, 4);
        this.interaction.addFieldValues("M1", "DEDE", "MM1", "SAL");

        this.runApp();

        assertThrownCommandException("UnknownProductKeyException", "O produto 'DEDE' não existe.");
        assertThrownCommandException("UnknownPartnerKeyException", "O parceiro 'MM1' não existe.");
        assertNoMoreExceptions();
        assertEquals("", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-10-03-M-ok - Adiciono um batch com um preço mais baixo e há notificação")
    void addBatchWithLowerPriceAndExpectBargainNotification() {
        super.loadFromInputFile("test033.input");
        this.interaction.addMenuOptions(7, 4, 0);
        this.interaction.addFieldValues("M1", "SAL", "50", "10"); // add acquisition transaction
        this.interaction.addMenuOptions(6, 1);
        this.interaction.addFieldValues("S1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                BARGAIN|SAL|50""", this.interaction.getResult());
    }

    @Test
    @DisplayName("A-10-04-M-ok - Bargain, vê parceiro, vê parceiro")
    void checkIfBargainNotificationIsCleared() {
        super.loadFromInputFile("test033.input");
        this.interaction.addMenuOptions(7, 4, 0);
        this.interaction.addFieldValues("M1", "SAL", "50", "10"); // add acquisition transaction
        this.interaction.addMenuOptions(6, 1, 1, 1, 1);
        this.interaction.addFieldValues("S1", "S1", "M2", "M2");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                BARGAIN|SAL|50
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                M2|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                BARGAIN|SAL|50
                M2|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0""", this.interaction.getResult());

    }

    @Test
    @DisplayName("A-10-05-M-ok - Bargain, vê parceiro, Bargain e vê parceiro")
    void sendBargainAfterBargainNotification() {
        super.loadFromInputFile("test033.input");
        this.interaction.addMenuOptions(7, 4, 0);
        this.interaction.addFieldValues("M1", "SAL", "50", "10"); // add acquisition transaction
        this.interaction.addMenuOptions(6, 1, 1, 0);
        this.interaction.addFieldValues("S1", "M2");
        this.interaction.addMenuOptions(7, 4, 0);
        this.interaction.addFieldValues("M1", "SAL", "2", "3"); // add acquisition transaction
        this.interaction.addMenuOptions(5, 1, 0, 6, 1, 1);
        this.interaction.addFieldValues("M2", "S1");

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                BARGAIN|SAL|50
                M2|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                BARGAIN|SAL|50
                HIDROGENIO|200|5000
                ROLHA|2000|500
                SAL|100|513
                VIDRO|1000|500
                M2|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                BARGAIN|SAL|2
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                BARGAIN|SAL|2""", this.interaction.getResult());

    }

}
