import * as vscode from 'vscode';

// తెలుగుఫ్యూజన్ కీలకపదాలు మరియు డేటా రకాలు
const తెలుగుఫ్యూజన్కీలకపదాలు = [
    'ప్రమేయం', 'చర', 'తిరిగిఇవ్వు', 'ఒకవేళ', 'లేకపోతే', 'కొరకు', 'అయ్యేవరకు',
    'స్థిరం', 'తరగతి', 'దిగుమతి', 'ఏజెంట్', 'నిజం', 'తప్పు', 'పూర్ణం', 'తేలియాడు',
    'బూలియన్', 'వాక్యం', 'అక్షరం', 'శూన్యం', 'జాబితా', 'నిఘంటువు', 'జత', 'వెక్టర్',
    'ప్రయత్నించు', 'పట్టుకో', 'చివరగా', 'విసురు', 'మాట్రిక్స్', 'సాంఖ్యిక', 'వెబ్సర్వర్'
];

const తెలుగుఫ్యూజన్డేటారకాలు = [
    'పూర్ణం', 'తేలియాడు', 'బూలియన్', 'వాక్యం', 'అక్షరం', 'శూన్యం', 'జాబితా', 'నిఘంటువు', 'జత', 'వెక్టర్'
];

const తెలుగుఫ్యూజన్స్నిప్పెట్లు: { [key: string]: { prefix: string, body: string[], description: string } } = {
    'ప్రమేయం': {
        prefix: 'ప్రమేయం',
        body: ['ప్రమేయం ${1:పేరు}(${2:పారామీటర్లు}) -> ${3:తిరిగిఇచ్చేరకం} {', '\t$0', '}'],
        description: 'ప్రమేయం నిర్వచనం'
    },
    'ఒకవేళ': {
        prefix: 'ఒకవేళ',
        body: ['ఒకవేళ (${1:షరతు}) {', '\t$0', '}'],
        description: 'ఒకవేళ ప్రకటన'
    },
    'కొరకు': {
        prefix: 'కొరకు',
        body: ['కొరకు (${1:ప్రారంభం}; ${2:షరతు}; ${3:వృద్ధి}) {', '\t$0', '}'],
        description: 'కొరకు లూప్'
    }
};

// సక్రియం చేయడం
export function activate(context: vscode.ExtensionContext) {
    console.log('తెలుగుఫ్యూజన్ VSCode ప్లగిన్ సక్రియమైంది');

    // కోడ్ పూర్తి ప్రదాత
    const completionProvider = vscode.languages.registerCompletionItemProvider('telugufusion', {
        provideCompletionItems(document: vscode.TextDocument, position: vscode.Position) {
            const linePrefix = document.lineAt(position).text.substr(0, position.character);
            const completionItems: vscode.CompletionItem[] = [];

            తెలుగుఫ్యూజన్కీలకపదాలు.forEach(keyword => {
                const item = new vscode.CompletionItem(keyword, vscode.CompletionItemKind.Keyword);
                item.detail = 'తెలుగుఫ్యూజన్ కీలకపదం';
                completionItems.push(item);
            });

            తెలుగుఫ్యూజన్డేటారకాలు.forEach(dataType => {
                const item = new vscode.CompletionItem(dataType, vscode.CompletionItemKind.TypeParameter);
                item.detail = 'తెలుగుఫ్యూజన్ డేటా రకం';
                completionItems.push(item);
            });

            Object.keys(తెలుగుఫ్యూజన్స్నిప్పెట్లు).forEach(key => {
                const snippet = తెలుగుఫ్యూజన్స్నిప్పెట్లు[key];
                const item = new vscode.CompletionItem(key, vscode.CompletionItemKind.Snippet);
                item.insertText = new vscode.SnippetString(snippet.body.join('\n'));
                item.documentation = new vscode.MarkdownString(snippet.description);
                completionItems.push(item);
            });

            return completionItems;
        }
    });

    context.subscriptions.push(completionProvider);

    // డయాగ్నోస్టిక్స్ ప్రదాత
    const diagnosticCollection = vscode.languages.createDiagnosticCollection('telugufusion');
    context.subscriptions.push(diagnosticCollection);

    // డాక్యుమెంట్ మార్పు వినికిడి
    vscode.workspace.onDidChangeTextDocument(event => {
        if (event.document.languageId === 'telugufusion') {
            updateDiagnostics(event.document, diagnosticCollection);
        }
    });

    // డీబగ్గర్ సెటప్
    const debugProvider = vscode.debug.registerDebugConfigurationProvider('telugufusion', {
        resolveDebugConfiguration(folder: vscode.WorkspaceFolder | undefined, config: vscode.DebugConfiguration, token?: vscode.CancellationToken): vscode.ProviderResult<vscode.DebugConfiguration> {
            if (!config.type && !config.request && !config.name) {
                const editor = vscode.window.activeTextEditor;
                if (editor && editor.document.languageId === 'telugufusion') {
                    config.type = 'telugufusion';
                    config.name = 'తెలుగుఫ్యూజన్ డీబగ్';
                    config.request = 'launch';
                    config.program = '${file}';
                    config.args = [];
                    config.cwd = '${workspaceFolder}';
                }
            }
            return config;
        }
    });

    context.subscriptions.push(debugProvider);

    // హోవర్ ప్రదాత
    const hoverProvider = vscode.languages.registerHoverProvider('telugufusion', {
        provideHover(document: vscode.TextDocument, position: vscode.Position) {
            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range);

            if (తెలుగుఫ్యూజన్కీలకపదాలు.includes(word)) {
                return new vscode.Hover(`${word} అనేది తెలుగుఫ్యూజన్ కీలకపదం`);
            }

            if (తెలుగుఫ్యూజన్డేటారకాలు.includes(word)) {
                return new vscode.Hover(`${word} అనేది తెలుగుఫ్యూజన్ డేటా రకం`);
            }

            return null;
        }
    });

    context.subscriptions.push(hoverProvider);
}

// డయాగ్నోస్టిక్స్ నవీకరణ
function updateDiagnostics(document: vscode.TextDocument, collection: vscode.DiagnosticCollection): void {
    const diagnostics: vscode.Diagnostic[] = [];

    for (let lineIndex = 0; lineIndex < document.lineCount; lineIndex++) {
        const lineOfText = document.lineAt(lineIndex);
        const lineText = lineOfText.text.trim();

        // ప్రతి పంక్తిలో ';' ఉందా?
        if (!lineText.endsWith(';') && !lineText.startsWith('//') && !lineText.startsWith('/*') && !lineText.endsWith('*/') && lineText !== '' && !lineText.endsWith('{') && !lineText.endsWith('}')) {
            diagnostics.push(new vscode.Diagnostic(
                lineOfText.range,
                "ప్రతి ప్రకటన ';'తో ముగియాలి",
                vscode.DiagnosticSeverity.Warning
            ));
        }

        // ప్రమేయం నిర్వచనం సరిగ్గా ఉందా?
        if (lineText.startsWith('ప్రమేయం') && !lineText.includes('->')) {
            diagnostics.push(new vscode.Diagnostic(
                lineOfText.range,
                "ప్రమేయం నిర్వచనంలో తిరిగి ఇచ్చే రకం తప్పనిసరి (ఉదా: -> పూర్ణం)",
                vscode.DiagnosticSeverity.Error
            ));
        }

        // చరరాశి ప్రకటన సరిగ్గా ఉందా?
        if (lineText.startsWith('చర') && !lineText.includes(':')) {
            diagnostics.push(new vscode.Diagnostic(
                lineOfText.range,
                "చరరాశి ప్రకటనలో రకం తప్పనిసరి (ఉదా: చర x: పూర్ణం = 5)",
                vscode.DiagnosticSeverity.Warning
            ));
        }
    }

    collection.set(document.uri, diagnostics);
}

// నిష్క్రియం చేయడం
export function deactivate() {
    console.log('తెలుగుఫ్యూజన్ VSCode ప్లగిన్ నిష్క్రియమైంది');
}
