package cakeelement;

import java.util.LinkedList;

public class Layer {
	public String position;
	public String diameter;
	public String hasCream;
	public String ingredientList;
	
	public Layer() {};
	
	public Layer(String position, String diameter, String hasCream, String ingredientList)
	{
		this.position = position;
		this.diameter = diameter;
		this.hasCream = hasCream;
		this.ingredientList = ingredientList;
		Integer.parseInt("2");
		
	}
}
