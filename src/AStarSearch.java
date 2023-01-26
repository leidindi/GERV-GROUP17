import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;




//We only have to worry about what is happening here and implement these functions

public class AStarSearch implements SearchAlgorithm {

	private Heuristics heuristics;
    //private HashMap<Integer, ArrayList<State>> myHashMap = new HashMap<Integer, ArrayList<State>>();

	private int nbNodeExpansions;
	private int maxFrontierSize;
	boolean success = false;
	int counter = 0;
    private ArrayList<Node> frontierList;

	int homeXcoordinates; 
	int homeYcoordinates;

	int surfaceSize = 0; //Ath

	private Node goalNode;

	public AStarSearch(Heuristics h) {
		this.heuristics = h; //we have this object that we can use (or implement our own)
		//Remember: node expansion is the same as state expansion in the instructions
		//use Heuristic informed search slides when implementing
		//slide number 2 is the basic of it - that is you still can improve it a lot
	}

	@Override
	public void doSearch(Environment env) {
		heuristics.init(env);
		nbNodeExpansions = 0;
		maxFrontierSize = 0;
		//goalNode = null;
		success = false;

		frontierList = new ArrayList<Node>();
		//myHashSet = new HashSet<>();

		Node currNode = new Node(env.getCurrentState(), heuristics.eval(env.getCurrentState()));
        frontierList.add(currNode);

		homeXcoordinates = currNode.state.position.x;
		homeYcoordinates = currNode.state.position.y;

		

		// TODO implement the search here
		// Update nbNodeExpansions and maxFrontierSize while doing the search:
		// - nbNodeExpansions should be incremented by one for each node popped from the frontier
		// - maxFrontierSize should be the largest size of the frontier observed during the search measured in number of nodes
		// Once a goal node has been found, set the goalNode variable to it, this should take care of getPlan() and getPlanCost() below,
		// as long as the node contains the right information.


		
	}

	@Override
	public List<Action> getPlan() {
		if (goalNode == null) return null;
		else return goalNode.getPlan();
	}

	@Override
	public int getNbNodeExpansions() {
		return nbNodeExpansions;
	}

	@Override
	public int getMaxFrontierSize() {
		return maxFrontierSize;
	}

	@Override
	public int getPlanCost() {
		if (goalNode != null) return goalNode.evaluation;
		else return 0;
	}

}
