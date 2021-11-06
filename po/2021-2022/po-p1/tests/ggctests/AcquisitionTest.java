package ggctests;

import ggctests.utils.PoUILibTest;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class AcquisitionTest extends PoUILibTest {

  public AcquisitionTest() {
    super(true);
  }

  protected void setupWarehouseManager() {
  }

  @Test
  @DisplayName("A-11-01-M-ok - Compra lote de produto simples existente com preço intermédio, vê transacção  ")
  @Disabled
  // TODO no idea where the esgotado.ggc file comes from, disabling until then
  void acquireSimpleProductViewTransaction() {
    loadFromInputFile("tests025.input");
    this.interaction.addMenuOptions(5, 1, 0, 7, 4, 1, 1, 0, 5, 1, 4);
    this.interaction.addFieldValues("M1", "SAL", "100", "10", "0", "1", "SAL");

    this.runApp();

    assertEquals("""
            HIDROGENIO|2|5000
            ROLHA|2|500
            SAL|1|0
            VIDRO|1|500
            VENDA|0|M1|SAL|10|10|10|2
            COMPRA|1|M1|SAL|10|1000|0
            HIDROGENIO|2|5000
            ROLHA|2|500
            SAL|100|10
            VIDRO|1|500
            SAL|M1|100|10""", this.interaction.getResult());
  }

}
