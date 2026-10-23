---
name: g03-dart-add-unit-test
description: Escribe y organiza tests unitarios de funciones, métodos y clases Dart con package:test. Usar al crear lógica nueva o al corregir un bug, para que el código siga funcionando.
metadata:
  tipo: skill
  area:
  - mobile
  - qa
  fase:
  - testing
  tecnologias:
  - dart
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '03'
  autor:
    nombre: Lautaro German Reinoso
    github: LautiGR116
  colaboradores:
  - nombre: Ignacio Nicolás Correa Rodríguez
    github: NachoCor2007
  responsables:
  - LautiGR116
  madurez: experimental
  relacionados: []
  model: models/gemini-3.1-pro-preview
  last_modified: Mon, 03 Aug 2026 21:51:24 GMT
---
# Testing Dart and Flutter Applications

## Contents
- [Structuring Test Files](#structuring-test-files)
- [Writing Tests](#writing-tests)
- [Executing Tests](#executing-tests)
- [Test Implementation Workflow](#test-implementation-workflow)
- [Examples](#examples)
- [Using This With Any Agent](#using-this-with-any-agent)

## Structuring Test Files
Organize test files to mirror the `lib` directory structure to maintain predictability.

* Place all test code within the `test` directory at the root of the package.
* Append `_test.dart` to the end of all test file names (e.g., `lib/src/utils.dart` should be tested in `test/src/utils_test.dart`).
* If writing integration tests, place them in an `integration_test` directory at the root of the package.

## Writing Tests
Utilize `package:test` as the standard testing library for Dart applications.

* Import `package:test/test.dart` (or `package:flutter_test/flutter_test.dart` for Flutter).
* Group related tests using the `group()` function to provide shared context.
* Define individual test cases using the `test()` function.
* Validate outcomes using the `expect()` function alongside matchers (e.g., `equals()`, `isTrue`, `throwsA()`).
* Write asynchronous tests using standard `async`/`await` syntax. The test runner automatically waits for the `Future` to complete.
* Manage test setup and teardown using `setUp()` and `tearDown()` callbacks.
* If testing code that relies on dependency injection, use `package:mockito` alongside `package:test` to generate mock objects, configure fixed scenarios, and verify interactions.

## Executing Tests
Select the appropriate test runner based on the project type and test location.

* If working on a pure Dart project, execute tests using the `dart test` command.
* If working on a Flutter project, execute tests using the `flutter test` command.
* If running integration tests, explicitly specify the directory path, as the default runner ignores it: `dart test integration_test` or `flutter test integration_test`.

## Test Implementation Workflow

Follow this sequential workflow when implementing new test suites. Copy the checklist to track your progress.

### Task Progress
- [ ] 1. Create the test file in the `test/` directory, ensuring the `_test.dart` suffix.
- [ ] 2. Import `package:test/test.dart` and the target library.
- [ ] 3. Define a `main()` function.
- [ ] 4. Initialize shared resources or mocks using `setUp()`.
- [ ] 5. Write `test()` cases grouped by functionality using `group()`.
- [ ] 6. Execute the test suite using the appropriate CLI command.
- [ ] 7. **Feedback Loop**: Run test -> Review stack trace for failures -> Fix implementation or assertions -> Re-run until passing.

## Examples

### Standard Unit Test Suite
Demonstrates grouping, setup, synchronous, and asynchronous testing.

```dart
import 'package:test/test.dart';
import 'package:my_package/calculator.dart';

void main() {
  group('Calculator', () {
    late Calculator calc;

    setUp(() {
      calc = Calculator();
    });

    test('adds two numbers correctly', () {
      expect(calc.add(2, 3), equals(5));
    });

    test('handles asynchronous operations', () async {
      final result = await calc.fetchRemoteValue();
      expect(result, isNotNull);
      expect(result, greaterThan(0));
    });
  });
}
```

### Mocking with Mockito
Demonstrates configuring a mock object for dependency injection testing.

```dart
import 'package:test/test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:my_package/api_client.dart';
import 'package:my_package/data_service.dart';

// Generate the mock using build_runner: dart run build_runner build
@GenerateNiceMocks([MockSpec<ApiClient>()])
import 'data_service_test.mocks.dart';

void main() {
  group('DataService', () {
    late MockApiClient mockApiClient;
    late DataService dataService;

    setUp(() {
      mockApiClient = MockApiClient();
      dataService = DataService(apiClient: mockApiClient);
    });

    test('returns parsed data on successful API call', () async {
      // Configure the mock
      when(mockApiClient.get('/data')).thenAnswer((_) async => '{"id": 1}');

      // Execute the system under test
      final result = await dataService.fetchData();

      // Verify outcomes and interactions
      expect(result.id, equals(1));
      verify(mockApiClient.get('/data')).called(1);
    });
  });
}
```

## Using This With Any Agent

Nothing in this file assumes Claude specifically — it's plain markdown with no tool syntax baked in. Point your agent at it directly: reference it from your agent's own project-instructions file (`AGENTS.md` for Codex CLI, `GEMINI.md` for Gemini CLI, or the equivalent for whatever you use), or just name the file path in your prompt. Works the same in Codex, Gemini, Claude, or no agent at all — reading it yourself.

## Ejemplo de uso

**Pedido:** "Agregá tests para la función que calcula cuánto debe cada participante."

**Resultado:** Un archivo de tests con los casos normales y los bordes (cero participantes, montos con decimales) agrupados y nombrados con claridad.
