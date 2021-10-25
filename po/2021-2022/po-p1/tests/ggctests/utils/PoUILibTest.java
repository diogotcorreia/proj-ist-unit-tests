package ggctests.utils;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.fail;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestInstance;

import pt.tecnico.uilib.Dialog;
import pt.tecnico.uilib.menus.CommandException;
import ggc.WarehouseManager;
import ggc.exceptions.ImportFileException;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public abstract class PoUILibTest {

  private boolean resetWarehouseManagerBeforeEach = false;
  private Dialog dialog;
  protected TestsInteraction interaction;
  protected WarehouseManager warehouseManager;

  public PoUILibTest() {
  }

  public PoUILibTest(boolean resetWarehouseManagerBeforeEach) {
    this.resetWarehouseManagerBeforeEach = resetWarehouseManagerBeforeEach;
  }

  protected abstract void setupWarehouseManager();

  @BeforeAll
  public void setupDialogInstance() {
    this.interaction = new TestsInteraction();
    this.dialog = new Dialog(interaction);
    Dialog.UI = this.dialog;

    if (!resetWarehouseManagerBeforeEach) {
      this.warehouseManager = new WarehouseManager();

      setupWarehouseManager();
    }
  }

  @BeforeEach
  public void resetTestsInteraction() {
    this.interaction.reset();

    if (resetWarehouseManagerBeforeEach) {
      this.warehouseManager = new WarehouseManager();

      setupWarehouseManager();
    }
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

  protected void assertNoMoreExceptions() {
    if (this.interaction.getCommandExceptions().size() != 0) {
      fail("Expected commands to not throw exceptions. The following exceptions were thrown: " + this.interaction.getCommandExceptions());
    }
  }

  protected void loadFromInputFile(String fileName) {
    try {
      this.warehouseManager.importFile("tests/resources/" + fileName);
    } catch (ImportFileException e) {
      fail("Could not import from file " + fileName);
    }
  }

  protected String getTextFromFile(String fileName) {
    try {
      return Files.readString(Path.of("tests/resources/" + fileName));
    } catch (IOException e) {
      fail("[Test Error] Could not load output from resource file " + fileName);
      return "";
    }
  }

}