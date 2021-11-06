package ggctests.utils;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestInstance;
import pt.tecnico.uilib.Dialog;
import pt.tecnico.uilib.menus.CommandException;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.fail;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public abstract class PoUILibTest {

    private static Class<?> warehouseManagerClass;
    private static Constructor<?> warehouseManagerConstructor;
    private static Method warehouseManagerImportFileMethod;
    private static Constructor<ggc.app.main.Menu> mainMenuConstructor;

    static {
      try {
        warehouseManagerClass = Class.forName("ggc.WarehouseManager");
      } catch (ClassNotFoundException e) {
        try {
          warehouseManagerClass = Class.forName("ggc.core.WarehouseManager");
        } catch (ClassNotFoundException ex) {
          fail("Could not find a WarehouseManager class to hook into. Searched at ggc.WarehouseManager and ggc.core.WarehouseManager", ex);
        }
      }
      try {
        warehouseManagerConstructor = warehouseManagerClass.getConstructor();
      } catch (NoSuchMethodException e) {
        fail("Could not find the default constructor for WarehouseManager. Make sure it has a public constructor without arguments", e);
      }

      try {
        warehouseManagerImportFileMethod = warehouseManagerClass.getMethod("importFile", String.class);
      } catch (NoSuchMethodException e) {
        fail("Could not find a public importFile(String) method on WarehouseManager", e);
      }

      try {
        mainMenuConstructor = ggc.app.main.Menu.class.getConstructor(warehouseManagerClass);
      } catch (NoSuchMethodException e) {
        fail("Could not find a constructor on main menu that takes a WarehouseManager", e);
      }

    }

    private boolean resetWarehouseManagerBeforeEach = false;
    private Dialog dialog;
    protected TestsInteraction interaction;
    /* Since Alameda and Tagus are using different packages for this, we're going to
       have to use reflection to correctly use this */
    protected Object warehouseManager;

    public PoUILibTest() {
    }

    public PoUILibTest(boolean resetWarehouseManagerBeforeEach) {
        this.resetWarehouseManagerBeforeEach = resetWarehouseManagerBeforeEach;
    }

    protected abstract void setupWarehouseManager();

    public Object newWarehouseManager() {
      try {
        return warehouseManagerConstructor.newInstance();
      } catch (InstantiationException | IllegalAccessException | InvocationTargetException e) {
        fail("Failed to instantiate a new WarehouseManager with a public empty constructor", e);
      }
      return null;
    }

    @BeforeAll
    public void setupDialogInstance() {
        this.interaction = new TestsInteraction();
        this.dialog = new Dialog(interaction);
        Dialog.UI = this.dialog;

        if (!resetWarehouseManagerBeforeEach) {
            this.warehouseManager = newWarehouseManager();

            setupWarehouseManager();
        }
    }

    @BeforeEach
    public void resetTestsInteraction() {
        this.interaction.reset();

        if (resetWarehouseManagerBeforeEach) {
            this.warehouseManager = newWarehouseManager();

            setupWarehouseManager();
        }
    }

    protected void runApp() {
      try {
          mainMenuConstructor.newInstance(this.warehouseManager).open();
      } catch (InstantiationException | IllegalAccessException | InvocationTargetException e) {
          fail("Failed to instantiate the main menu with the WarehouseManager", e);
      }
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
            warehouseManagerImportFileMethod.invoke(this.warehouseManager, "tests/resources/" + fileName);
        } catch (InvocationTargetException | IllegalAccessException e) {
            fail("Failed to invoke importFile method via reflection", e);
        } catch (Exception e) { /* have to use a generic exception because of reflection */
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