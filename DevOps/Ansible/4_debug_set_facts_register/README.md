# Переменные `Debug`, `Set_fact` и `Register`

## `Debug`

Данная переменная служит для дебаггинга, вывода значений, содержащихся в переменных или просто сообщений.

```cmd
- name: Print variable value
  debug:
    var: <variable_name>
```

```cmd
- name: Print message
  debug:
    msg: "System {{ inventory_hostname }} has gateway {{ ansible_default_ipv4.gateway }}"
```

## `Set_fact`

Создает новую переменную с значением (фактом).

```cmd
# Example setting host facts using key=value pairs, note that this always creates strings or booleans
- set_fact: one_fact="something" other_fact="{{ local_var }}"

# Example setting host facts using complex arguments
- set_fact:
     one_fact: something
     other_fact: "{{ local_var * 2 }}"
     another_fact: "{{ some_registered_var.results | map(attribute='ansible_facts.some_fact') | list }}"

# Example setting facts so that they will be persisted in the fact cache
- set_fact:
    one_fact: something
    other_fact: "{{ local_var * 2 }}"
    cacheable: true

# As of 1.8, Ansible will convert boolean strings ('true', 'false', 'yes', 'no')
# to proper boolean values when using the key=value syntax, however it is still
# recommended that booleans be set using the complex argument style:
- set_fact:
    one_fact: true
    other_fact: false
```

## `Register`

Это нужно для того, чтобы вывести какой-то результат, который не отображается, например, после команды `-shell: uptime` мы получим информацию о том, что есть изменения, но не выведет какую-либо информацию. Поэтому этот результат мы регистрируем и с помощью `debug` сможем в любом случае посмотреть на содержимое результата.

```cmd
... playbook ...

- shell: uptime
  register: result

- debug:
    var: result
```

