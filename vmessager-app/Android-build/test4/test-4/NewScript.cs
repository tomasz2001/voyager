using Godot;
using System;
using System.Threading.Tasks;
using EdjCase.ICP.Agent;
using EdjCase.ICP.Agent.Agents;
using EdjCase.ICP.Candid.Models;

public partial class NewScript : Node
{
	private Label _resultLabel;

	public override void _Ready()
	{
		// Pobierz referencję do Labela (dziecko o nazwie ResultLabel)
		_resultLabel = GetNode<Label>("ResultLabel");

		// Startujemy asynchroniczną pętlę
		_ = StartLoop();
	}

	private async Task StartLoop()
	{
		var agent = new HttpAgent();
		Principal princ = Principal.FromText("e6lpp-6iaaa-aaaaa-qajnq-cai");   // id kanistra
		var metoda = "dataShow"; // nazwa metody
		ulong updateArgument = 1000;

		CandidArg ar = CandidArg.FromCandid(CandidTypedValue.Nat(updateArgument));

		while (true) // nieskończona pętla
		{
			try
			{
				var odpowiedz = await agent.CallAndWaitAsync(princ, metoda, ar);

				// Ustaw tekst na ekranie (na środku)
				_resultLabel.Text = $"Odpowiedź kanistra:\n{odpowiedz}";
			}
			catch (Exception ex)
			{
				_resultLabel.Text = $"Błąd:\n{ex.Message}";
			}

			await Task.Delay(1000); // odczekaj 1 sekundę
		}
	}
}
