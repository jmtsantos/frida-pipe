# frida-pipe

A python script that lets you pipe ouput from stdin directly into a frida script.


## Instalation

Just make sure your frida instalation is up to date and you should be goood to go.

## Usage

The script reads directly from `stdin` so you can pipe whatever input into the frida script, just make sure that whatever changes you make to `piper.js` the export name stays the same.

A common use case would be to decode obfuscated/encripted strings in an Android application. Lets say that class `com.package.with.decoder` holds a method `a` that deobfuscates the strings.

So we edit the `piper.js` to call that same method and print out the output:

```
rpc.exports = {
    decodenative: function decodenative(str) {
        Java.perform(function () {
            var appClass = Java.use('com.package.with.decoder').$new();
            send(str + " - > " + appClass.method(str));
        })
    }
}
```

Then we can just call the script to run over the obfuscated strings `cat strings.txt | python piper.py`.