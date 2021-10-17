package ggctests.utils;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.fail;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestInstance;

import pt.tecnico.uilib.Dialog;
import pt.tecnico.uilib.menus.CommandException;
import ggc.WarehouseManager;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public abstract class PoUILibTest {

  private Dialog dialog;
  protected TestsInteraction interaction;
  protected WarehouseManager warehouseManager;

  protected abstract void setupWarehouseManager();

  @BeforeAll
  public void setupDialogInstance() {
    this.interaction = new TestsInteraction();
    this.dialog = new Dialog(interaction);
    Dialog.UI = this.dialog;

    this.warehouseManager = new WarehouseManager();

    setupWarehouseManager();
  }

  @BeforeEach
  public void resetTestsInteraction() {
    this.interaction.reset();
  }

  protected void runApp() {
    new ggc.app.main.Menu(this.warehouseManager).open();
  }

  @AfterAll
  public void closeDialog() {
    this.dialog.close();
  }

  protected void assertThrownCommandException(Class<? extends CommandException> clazz, String msg) {
    if (this.interaction.getCommandExceptions().size() == 0) {
      fail("Exception " + clazz.getName() + " was not thrown");
    }

    CommandException ce = this.interaction.getCommandExceptions().remove();
    assertInstanceOf(clazz, ce);
    assertEquals("Operação inválida: " + msg, ce.toString());
  }

}