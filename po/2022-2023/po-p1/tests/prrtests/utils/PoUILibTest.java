package prrtests.utils;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestInstance;

import prr.NetworkManager;
import prr.exceptions.ImportFileException;
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

    // FIXME 
    // Not sure how this years Tagus source is, I commented it out to make it simpler and get the repo going

    // private static Class<?> networkManagerClass;
    // private static Constructor<?> networkManagerConstructor;
    // private static Method networkManagerImportFileMethod;
    // private static Constructor<ggc.app.main.Menu> mainMenuConstructor;

    // static {
    //     try {
    //         networkManagerClass = tryClassNames("ggc.NetworkManager", "ggc.core.NetworkManager");
    //     } catch (ClassNotFoundException e) {
    //         fail("Could not find a NetworkManager class to hook into. Searched at ggc.NetworkManager and ggc.core.NetworkManager", e);
    //     }

    //     try {
    //         networkManagerConstructor = networkManagerClass.getConstructor();
    //     } catch (NoSuchMethodException e) {
    //         fail("Could not find the default constructor for NetworkManager. Make sure it has a public constructor without arguments", e);
    //     }

    //     try {
    //         networkManagerImportFileMethod = networkManagerClass.getMethod("importFile", String.class);
    //     } catch (NoSuchMethodException e) {
    //         fail("Could not find a public importFile(String) method on NetworkManager", e);
    //     }

    //     try {
    //         mainMenuConstructor = ggc.app.main.Menu.class.getConstructor(networkManagerClass);
    //     } catch (NoSuchMethodException e) {
    //         fail("Could not find a constructor on main menu that takes a NetworkManager", e);
    //     }
    // }

    private boolean resetNetworkManagerBeforeEach = false;
    private Dialog dialog;
    protected TestsInteraction interaction;
    /* Since Alameda and Tagus are using different packages for this, we're going to
       have to use reflection to correctly use this */
    protected NetworkManager networkManager;

    public PoUILibTest() {
    }

    public PoUILibTest(boolean resetNetworkManagerBeforeEach) {
        this.resetNetworkManagerBeforeEach = resetNetworkManagerBeforeEach;
    }

    protected abstract void setupNetworkManager();

    // public Object newNetworkManager() {
    //     try {
    //         return networkManagerConstructor.newInstance();
    //     } catch (InstantiationException | IllegalAccessException | InvocationTargetException e) {
    //         fail("Failed to instantiate a new NetworkManager with a public empty constructor", e);
    //     }
    //     return null;
    // }

    @BeforeAll
    public void setupDialogInstance() {
        this.interaction = new TestsInteraction();
        this.dialog = new Dialog(interaction);
        Dialog.UI = this.dialog;

        if (!resetNetworkManagerBeforeEach) {
            this.networkManager = new NetworkManager();

            setupNetworkManager();
        }
    }

    @BeforeEach
    public void resetTestsInteraction() {
        this.interaction.reset();

        if (resetNetworkManagerBeforeEach) {
            this.networkManager = new NetworkManager();

            setupNetworkManager();
        }
    }

    protected void runApp() {
        new prr.app.main.Menu(this.networkManager).open();
    //   try {
    //       mainMenuConstructor.newInstance(this.networkManager).open();
    //   } catch (InstantiationException | IllegalAccessException | InvocationTargetException e) {
    //       fail("Failed to instantiate the main menu with the NetworkManager", e);
    //   }
    }

    @AfterAll
    public void closeDialog() {
        this.dialog.close();
    }

    // protected void assertThrownCommandException(String className, String msg) {
    //     Class<? extends CommandException> clazz = getCommandException(className);
    //     if (this.interaction.getCommandExceptions().size() == 0) {
    //         fail("Exception " + clazz.getName() + " was not thrown");
    //     }

    //     CommandException ce = this.interaction.getCommandExceptions().remove();
    //     assertInstanceOf(clazz, ce);
    //     assertEquals("Operação inválida: " + msg, ce.toString());
    // }
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

    // protected void loadFromInputFile(String fileName) {
    //     try {
    //         networkManagerImportFileMethod.invoke(this.networkManager, "tests/resources/" + fileName);
    //     } catch (InvocationTargetException | IllegalAccessException e) {
    //         fail("Failed to invoke importFile method via reflection", e);
    //     } catch (Exception e) { /* have to use a generic exception because of reflection */
    //         fail("Could not import from file " + fileName);
    //     }
    // }
    protected void loadFromInputFile(String fileName) {
        try {
            networkManager.importFile("tests/resources/" + fileName);
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

    // @SuppressWarnings("unchecked")
    // private Class<? extends CommandException> getCommandException(String name) {
    //   try {
    //       return (Class<? extends CommandException>) tryClassNames("ggc.app.exceptions." + name, "ggc.app.exception." + name);
    //   } catch (ClassNotFoundException e) {
    //       fail("Could not find app exception (" + name + ") via reflection", e);
    //   }
    //   return null;
    // }

    // private static Class<?> tryClassNames(String... classNames) throws ClassNotFoundException {
    //     for (String c : classNames) {
    //       try {
    //         return Class.forName(c);
    //       } catch (ClassNotFoundException ignore) {
    //         // try next class
    //       }
    //     }
    //     throw new ClassNotFoundException(classNames[0]);
    // }

}