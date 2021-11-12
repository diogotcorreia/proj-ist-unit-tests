package ggctests.utils;

import pt.tecnico.uilib.InteractionDriver;
import pt.tecnico.uilib.forms.Field;
import pt.tecnico.uilib.forms.Form;
import pt.tecnico.uilib.menus.CommandException;
import pt.tecnico.uilib.menus.Menu;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.Queue;
import java.util.StringJoiner;

/**
 * Tests interaction back-end (for Unit Tests).
 */
public class TestsInteraction implements InteractionDriver {

    /* Input parameters */
    private Queue<Integer> menuOptions = new LinkedList<>();
    private Queue<String> fieldValues = new LinkedList<>();

    /* Output results */
    private StringJoiner result = new StringJoiner("\n");
    private Queue<CommandException> commandExceptions = new LinkedList<>();

    /**
     * @see pt.tecnico.uilib.InteractionDriver#close()
     */
    @Override
    public void close() {

    }

    /**
     * @see pt.tecnico.uilib.InteractionDriver#open(pt.tecnico.uilib.menus.Menu)
     */
    @Override
    public void open(Menu menu) {
        int option = 0;

        while (true) {
            try {
                if (menuOptions.size() == 0)
                    return;

                option = menuOptions.remove();
                if (option == 0)
                    return;

                if (option < 0 || option > menu.size() || !menu.entry(option - 1).isValid()) {
                    throw new RuntimeException("Option " + option + " is not in the menu");
                } else {
                    menu.entry(option - 1).performCommand();
                    if (menu.entry(option - 1).isLast())
                        return;
                }
            } catch (CommandException e) {
                this.commandExceptions.add(e);
            }
        }
    }

    /**
     * @see pt.tecnico.uilib.InteractionDriver#fill(pt.tecnico.uilib.forms.Form)
     */
    @Override
    public void fill(Form form) {
        for (Field<?> in : form.entries()) {
            if (!in.isReadOnly()) {
                if (fieldValues.size() == 0)
                    throw new RuntimeException("Command is asking for more fields than expected");

                String value = fieldValues.remove();
                if (!in.parse(value))
                    throw new RuntimeException("Field " + in.prompt() + " was expecting a different value type. Received '" + value + "'");
            }
        }
    }

    /**
     * @see pt.tecnico.uilib.InteractionDriver#render(String, String)
     */
    @Override
    public void render(String title, String text) {
        if (text.length() > 0)
            result.add(text);
    }

    public void reset() {
        this.menuOptions = new LinkedList<>();
        this.fieldValues = new LinkedList<>();
        this.result = new StringJoiner("\n");
        this.commandExceptions = new LinkedList<>();
    }

    public void addMenuOptions(Integer... options) {
        Arrays.stream(options).forEach(option -> this.menuOptions.add(option));
    }

    public void addFieldValues(String... values) {
        Arrays.stream(values).forEach(value -> this.fieldValues.add(value));
    }

    public String getResult() {
        return this.result.toString();
    }

    public Queue<CommandException> getCommandExceptions() {
        return this.commandExceptions;
    }

}
