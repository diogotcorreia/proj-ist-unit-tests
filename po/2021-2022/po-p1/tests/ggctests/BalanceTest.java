package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class BalanceTest extends PoUILibTest{


    public BalanceTest() {
        super(true);
    }

    @Override
    protected void setupWarehouseManager() {
    }

    @Test
    @DisplayName("Partner NORMAL buys and sells simple products")
    void sellSimpleProductAlongTimeNormal() {
        super.loadFromInputFile("test039.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(0, 9, 4); // 0
        this.interaction.addFieldValues("2"); //2
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("3"); // 5
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //6 change P2
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("4");// 10
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //11 change P3
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //12
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("2"); //14
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //15
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1");// 16 change P4
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); // 17
        this.interaction.addMenuOptions(9, 7, 5);
        this.interaction.addFieldValues("0"); // pay
        this.interaction.addMenuOptions(0, 9);
        this.interaction.addFieldValues("30"); // see if value changed
        this.interaction.addMenuOptions(9, 4, 3); // it shouldn't

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 5
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 6
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 10
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 11
                Saldo dispon??vel: 0
                Saldo contabil??stico: 420
                Data actual: 12
                Saldo dispon??vel: 0
                Saldo contabil??stico: 440
                Data actual: 14
                Saldo dispon??vel: 0
                Saldo contabil??stico: 480
                Data actual: 15
                Saldo dispon??vel: 0
                Saldo contabil??stico: 500
                Data actual: 16
                Saldo dispon??vel: 0
                Saldo contabil??stico: 640
                Data actual: 17
                Saldo dispon??vel: 0
                Saldo contabil??stico: 680
                Saldo dispon??vel: 680
                Saldo contabil??stico: 680
                Saldo dispon??vel: 680
                Saldo contabil??stico: 680
                Data actual: 47""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner SELECTION buys and sells simple product")
    void sellSimpleProductAlongTimeSelection() {
        super.loadFromInputFile("test039.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "VIDRO", "1");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("M1","VIDRO","900","1");
        this.interaction.addMenuOptions(0, 9, 6, 2, 0, 7, 3); // 0
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(0, 9, 4); // 0
        this.interaction.addFieldValues("2"); //2
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("3"); // 5
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //6 change P2
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1");// 7
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1");// 8
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1");// 9 no discount
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1");// 10 no discount
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //11 change P3
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //12
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("2"); //14
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); //15
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1");// 16 change P4
        this.interaction.addMenuOptions(9, 4, 3);
        this.interaction.addFieldValues("1"); // 17
        this.interaction.addMenuOptions(9, 7, 5);
        this.interaction.addFieldValues("2"); // pay
        this.interaction.addMenuOptions(0, 9);
        this.interaction.addFieldValues("30"); // see if value changed
        this.interaction.addMenuOptions(9, 4, 3); // it shouldn't

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                Saldo dispon??vel: 0
                Saldo contabil??stico: 0
                M1|Rohit Figueiredo|New Delhi, India|SELECTION|9000|900|1000|900
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 5
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 6
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 7
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 8
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 9
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 10
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 11
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 12
                Saldo dispon??vel: 0
                Saldo contabil??stico: 416
                Data actual: 14
                Saldo dispon??vel: 0
                Saldo contabil??stico: 432
                Data actual: 15
                Saldo dispon??vel: 0
                Saldo contabil??stico: 440
                Data actual: 16
                Saldo dispon??vel: 0
                Saldo contabil??stico: 520
                Data actual: 17
                Saldo dispon??vel: 0
                Saldo contabil??stico: 540
                Saldo dispon??vel: 540
                Saldo contabil??stico: 540
                Saldo dispon??vel: 540
                Saldo contabil??stico: 540
                Data actual: 47""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner ELITE buys and sells simple product")
    void sellSimpleProductAlongTimeElite() {
        super.loadFromInputFile("test039.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "VIDRO", "3");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("M1","VIDRO","900","3");
        this.interaction.addMenuOptions(0,9,6,2,0,7,3); // 0
        this.interaction.addFieldValues("M1","10", "HIDROGENIO", "2");
        this.interaction.addMenuOptions(0,9,4); // 0
        this.interaction.addFieldValues("2"); //2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("3"); // 5
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //6 change P2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 7
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 8
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 9 no discount
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 10 no discount
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //11 change P3
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //12
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("2"); //14
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //15
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 16 change P4
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); // 17
        this.interaction.addMenuOptions(9,7,5);
        this.interaction.addFieldValues("2"); // pay
        this.interaction.addMenuOptions(0,9);
        this.interaction.addFieldValues("30"); // see if value changed
        this.interaction.addMenuOptions(9,4,3); // it shouldn't

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                Saldo dispon??vel: 0
                Saldo contabil??stico: 0
                M1|Rohit Figueiredo|New Delhi, India|ELITE|27000|2700|3000|2700
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 5
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 6
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 7
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 8
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 9
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 10
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 11
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 12
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 14
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 15
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 16
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 17
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Saldo dispon??vel: 400
                Saldo contabil??stico: 400
                Saldo dispon??vel: 400
                Saldo contabil??stico: 400
                Data actual: 47""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner NORMAL buys and sells derived product")
    void sellDerivedProductAlongTimeNormal() {
        super.loadFromInputFile("test040.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "MOLOTOV", "2");
        this.interaction.addMenuOptions(0,9,4); // 0
        this.interaction.addFieldValues("2"); //2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("5"); // 7
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //8 change P2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 9
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 10
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //11 change P3
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //12
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //13
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //14 change P$
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 15
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); // 16
        this.interaction.addMenuOptions(9,7,5);
        this.interaction.addFieldValues("0"); // pay
        this.interaction.addMenuOptions(0,9);
        this.interaction.addFieldValues("30"); // see if value changed
        this.interaction.addMenuOptions(9,4,3); // it shouldn't

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 7
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 8
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 9
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 10
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 11
                Saldo dispon??vel: 0
                Saldo contabil??stico: 420
                Data actual: 12
                Saldo dispon??vel: 0
                Saldo contabil??stico: 440
                Data actual: 13
                Saldo dispon??vel: 0
                Saldo contabil??stico: 460
                Data actual: 14
                Saldo dispon??vel: 0
                Saldo contabil??stico: 560
                Data actual: 15
                Saldo dispon??vel: 0
                Saldo contabil??stico: 600
                Data actual: 16
                Saldo dispon??vel: 0
                Saldo contabil??stico: 640
                Saldo dispon??vel: 640
                Saldo contabil??stico: 640
                Saldo dispon??vel: 640
                Saldo contabil??stico: 640
                Data actual: 46""", this.interaction.getResult());
    }

    @Test
    @DisplayName("Partner SELECTION buys and sells derived product")
    void sellDerivedProductAlongTimeSelection() {
        super.loadFromInputFile("test040.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1","10", "VIDRO", "1");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("M1","VIDRO","900","1");
        this.interaction.addMenuOptions(0,9,6,2,0,7,3); // 0
        this.interaction.addFieldValues("M1","10", "MOLOTOV", "2");
        this.interaction.addMenuOptions(0,9,4); // 0
        this.interaction.addFieldValues("2"); //2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("5"); // 7
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //8 change P2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 9
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 10
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //11 change P3
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //12
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //13
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //14 change P4
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 15
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); // 16
        this.interaction.addMenuOptions(9,7,5);
        this.interaction.addFieldValues("2"); // pay
        this.interaction.addMenuOptions(0,9);
        this.interaction.addFieldValues("30"); // see if value changed
        this.interaction.addMenuOptions(9,4,3); // it shouldn't

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                Saldo dispon??vel: 0
                Saldo contabil??stico: 0
                M1|Rohit Figueiredo|New Delhi, India|SELECTION|9000|900|1000|900
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 7
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 8
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 9
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 10
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 11
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 12
                Saldo dispon??vel: 0
                Saldo contabil??stico: 416
                Data actual: 13
                Saldo dispon??vel: 0
                Saldo contabil??stico: 424
                Data actual: 14
                Saldo dispon??vel: 0
                Saldo contabil??stico: 480
                Data actual: 15
                Saldo dispon??vel: 0
                Saldo contabil??stico: 500
                Data actual: 16
                Saldo dispon??vel: 0
                Saldo contabil??stico: 520
                Saldo dispon??vel: 520
                Saldo contabil??stico: 520
                Saldo dispon??vel: 520
                Saldo contabil??stico: 520
                Data actual: 46""", this.interaction.getResult());
    }


    @Test
    @DisplayName("Partner ELITE buys and sells derived product")
    void sellDerivedProductAlongTimeElite() {
        super.loadFromInputFile("test040.input");
        this.interaction.addMenuOptions(7, 3);
        this.interaction.addFieldValues("M1", "10", "VIDRO", "3");
        this.interaction.addMenuOptions(5);
        this.interaction.addFieldValues("0");
        this.interaction.addMenuOptions(4);
        this.interaction.addFieldValues("M1", "VIDRO","900","3");
        this.interaction.addMenuOptions(0,9,6,2,0,7,3); // 0
        this.interaction.addFieldValues("M1", "10", "MOLOTOV", "2");
        this.interaction.addMenuOptions(0,9,4); // 0
        this.interaction.addFieldValues("2"); //2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("5"); // 7
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //8 change P2
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 9
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 10
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //11 change P3
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //12
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //13
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); //14 change P$
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1");// 15
        this.interaction.addMenuOptions(9,4,3);
        this.interaction.addFieldValues("1"); // 16
        this.interaction.addMenuOptions(9,7,5);
        this.interaction.addFieldValues("2"); // pay
        this.interaction.addMenuOptions(0,9);
        this.interaction.addFieldValues("30"); // see if value changed
        this.interaction.addMenuOptions(9,4,3); // it shouldn't

        this.runApp();

        assertNoMoreExceptions();
        assertEquals("""
                Saldo dispon??vel: 0
                Saldo contabil??stico: 0
                M1|Rohit Figueiredo|New Delhi, India|ELITE|27000|2700|3000|2700
                S1|Toshiba|Tokyo, Japan|NORMAL|0|0|0|0
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 7
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 8
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 9
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 10
                Saldo dispon??vel: 0
                Saldo contabil??stico: 360
                Data actual: 11
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 12
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 13
                Saldo dispon??vel: 0
                Saldo contabil??stico: 380
                Data actual: 14
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 15
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Data actual: 16
                Saldo dispon??vel: 0
                Saldo contabil??stico: 400
                Saldo dispon??vel: 400
                Saldo contabil??stico: 400
                Saldo dispon??vel: 400
                Saldo contabil??stico: 400
                Data actual: 46""", this.interaction.getResult());
    }

}
